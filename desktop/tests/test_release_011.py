import copy
from pathlib import Path
import random
import sys
import unittest
from unittest.mock import MagicMock,patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from PySide6.QtCore import QPoint,QRect,QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from chunxi.config import DESKTOP_ROOT,load_config
from chunxi.display import visible_position
from chunxi.settings import SettingsDialog
from chunxi import startup


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])

    def test_negative_monitor_and_unplugged_screen_recovery(self):
        screens=[QRect(-1920,0,1920,1080),QRect(0,0,2560,1400)]
        size=QSize(192,208)
        self.assertEqual(visible_position(QPoint(-1000,400),size,screens),QPoint(-1000,400))
        moved=visible_position(QPoint(-1000,400),size,screens[1:])
        self.assertTrue(screens[1].contains(QRect(moved,size)))
        edge=visible_position(QPoint(2500,1390),size,screens)
        self.assertTrue(screens[1].contains(QRect(edge,size)))

    def test_settings_defaults_and_roundtrip(self):
        config=load_config()
        dialog=SettingsDialog(config,False)
        self.assertFalse(dialog.startup.isChecked())
        dialog.size.setValue(150);dialog.topmost.setChecked(False)
        dialog.frequency.setCurrentIndex(dialog.frequency.findData('quiet'))
        selected=dialog.selected_config()
        self.assertEqual(selected['window']['scale'],1.5)
        self.assertFalse(selected['window']['always_on_top'])
        self.assertEqual(selected['preferences']['frequency'],'quiet')
        self.assertEqual(config['window']['scale'],1.0)

    def test_startup_only_modifies_own_value_when_explicit(self):
        fake=MagicMock()
        fake.REG_SZ=1;fake.KEY_SET_VALUE=2
        fake.QueryValueEx.side_effect=FileNotFoundError
        with patch.dict(sys.modules,{'winreg':fake}),patch.object(startup.sys,'platform','win32'):
            self.assertFalse(startup.is_enabled())
            fake.SetValueEx.assert_not_called()
            startup.set_enabled(True)
            self.assertEqual(fake.SetValueEx.call_args.args[1],startup.VALUE)
            self.assertIn('--autostart',fake.SetValueEx.call_args.args[-1])
            fake.QueryValueEx.side_effect=None
            fake.QueryValueEx.return_value=(startup.command(),fake.REG_SZ)
            startup.set_enabled(False)
            self.assertEqual(fake.DeleteValue.call_args.args[1],startup.VALUE)

    def test_formal_multisize_icon(self):
        icon=QIcon(str(DESKTOP_ROOT/'assets/chunxi.ico'))
        self.assertFalse(icon.isNull())
        self.assertGreaterEqual(len(icon.availableSizes()),5)

    def test_startup_custom_profile_is_retained_in_command(self):
        profile = DESKTOP_ROOT / 'config/custom-example.json'
        value = startup.command(profile)
        self.assertIn('--config', value)
        self.assertIn(str(profile.resolve()), value)
