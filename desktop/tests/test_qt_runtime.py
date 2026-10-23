import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import math
from pathlib import Path
import random
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from chunxi.config import DESKTOP_ROOT, load_config
from chunxi.interaction import ActivityMonitor, DragGesture, direction_for
from chunxi.animation import SpriteLibrary
from chunxi.state_machine import State
from chunxi.window import PetWindow
from chunxi.settings import SizeDialog
from PySide6.QtCore import QTimer
from unittest.mock import patch
import copy


class QtRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = PetWindow(load_config(), persist=False, rng=random.Random(6))
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()

    def test_transparency_topmost_and_no_focus(self):
        w = self.window
        self.assertTrue(w.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground))
        for flag in (Qt.WindowType.WindowStaysOnTopHint, Qt.WindowType.FramelessWindowHint, Qt.WindowType.WindowDoesNotAcceptFocus):
            self.assertTrue(w.windowFlags() & flag)
        image = w.render_frame(time.monotonic())
        self.assertEqual(image.pixelColor(0, 0).alpha(), 0)
        self.assertFalse(w.mask().isEmpty())

    def test_all_clips_valid_and_no_empty_frame(self):
        for key, clip in self.window.library.clips.items():
            for image in clip.frames:
                self.assertEqual((image.width(), image.height()), (192, 208))
                self.assertTrue(image.hasAlphaChannel())
                self.assertFalse(image.isNull())
            self.assertEqual(clip.frame_at(0), clip.frames[0])
            self.assertEqual(clip.frame_at(sum(clip.durations_ms)+1), clip.frames[0] if clip.loop else clip.frames[-1])

    def test_direction_convention_and_drag_threshold(self):
        center = QPoint(100, 100)
        for point, direction in [(QPoint(100,0),0),(QPoint(200,100),4),(QPoint(100,200),8),(QPoint(0,100),12)]:
            self.assertEqual(direction_for(point, center), direction)
        drag = DragGesture(6)
        drag.press(QPoint(20,20),QPoint(100,100))
        self.assertIsNone(drag.move(QPoint(21,21)))
        self.assertEqual(drag.move(QPoint(60,70)),QPoint(140,150))
        self.assertTrue(drag.release())

    def test_real_qt_drag_suppresses_click(self):
        w = self.window
        w.machine.config['click_probability'] = 1
        before = w.pos()
        QTest.mousePress(w, Qt.MouseButton.LeftButton, pos=QPoint(96,145))
        QTest.mouseMove(w, QPoint(116,160))
        QTest.mouseRelease(w, Qt.MouseButton.LeftButton, pos=QPoint(116,160))
        self.assertNotEqual(w.pos(), before)
        self.assertEqual(w.machine.state, State.SITTING)
        self.assertIsNone(w.machine.action)

    def test_transition_does_not_render_blank(self):
        w = self.window
        now = time.monotonic()
        w.animator.select('loaf', 0, now)
        for offset in (0,0.15,0.3,0.5,0.7):
            frame = w.render_frame(now+offset)
            self.assertEqual(frame,w.library.get('loaf').frame_at(offset*1000))
            count = sum(frame.pixelColor(x,y).alpha()>0 for y in range(208) for x in range(192))
            self.assertGreater(count,1000)

    def test_preferences_apply_without_resetting_pose(self):
        import copy
        window=self.window
        config=copy.deepcopy(window.config)
        config['window']['scale']=1.5
        config['window']['always_on_top']=False
        config['preferences']['frequency']='quiet'
        old_state=window.machine.state
        window.apply_preferences(config)
        self.assertEqual(window.width(),288)
        self.assertEqual(window.machine.state,old_state)
        self.assertFalse(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
        self.assertEqual(window.machine.frequency_multiplier,1.5)

    def test_state_changes_keep_window_position_and_single_frame(self):
        now=time.monotonic();before=self.window.pos()
        for key in ('loaf','sleep','wake','look','blink','breathing'):
            self.window.animator.select(key,4,now)
            for elapsed in (0,.123,.357,.719):
                self.assertEqual(self.window.render_frame(now+elapsed),self.window.library.get(key,4).frame_at(elapsed*1000))
                self.assertEqual(self.window.pos(),before)

    def test_native_activity_api(self):
        monitor = ActivityMonitor()
        active, position = monitor.poll()
        self.assertIsInstance(active,bool)
        self.assertIsInstance(position,QPoint)
        if sys.platform == 'win32':
            self.assertIsNotNone(monitor._stamp())

    def test_rest_pose_registration_and_transparent_edges(self):
        bounds = {}
        for key in ('neutral','loaf','sleep'):
            boxes = []
            for frame in self.window.library.get(key).frames:
                points = [(x,y) for y in range(208) for x in range(192) if frame.pixelColor(x,y).alpha() > 0]
                left, right = min(x for x,y in points), max(x for x,y in points)
                bottom = max(y for x,y in points)
                self.assertGreater(left, 0)
                self.assertLess(right, 191)
                self.assertLess(bottom, 207)
                boxes.append((right-left+1,bottom))
            bounds[key] = boxes
        reference = bounds['neutral'][0][1]
        self.assertTrue(all(abs(bottom-reference)<=2 for boxes in bounds.values() for width,bottom in boxes))
        ratio = max(width for width,bottom in bounds['sleep']) / max(width for width,bottom in bounds['loaf'])
        self.assertLess(ratio, 1.1)

    def test_context_menu_quit_closes_window_and_timer(self):
        action = next(a for a in self.window.menu.actions() if a.text() == '退出春喜')
        action.trigger()
        self.assertFalse(self.window.isVisible())
        self.assertFalse(self.window.timer.isActive())

    def test_pause_menu_labels_and_current_config_path(self):
        self.window.pause_action.setChecked(True)
        self.assertTrue(self.window.machine.paused)
        self.assertIn('已暂停', self.window.pause_action.text())
        self.window.pause_action.setChecked(False)
        self.assertFalse(self.window.machine.paused)
        self.assertEqual(self.window.pause_action.text(), '暂停自动行为')
        target = DESKTOP_ROOT / 'build' / 'custom-config.json'
        self.window.config_path = target
        with patch('chunxi.window.QDesktopServices.openUrl', return_value=True) as open_url:
            self.window.open_config()
        self.assertEqual(Path(open_url.call_args.args[0].toLocalFile()), target.resolve())

    def test_large_finite_radius_does_not_overflow_during_poll(self):
        self.window.config['behavior']['near_radius_pixels'] = 1e300
        self.window._last_poll = 0
        self.window._tick()
        self.assertTrue(self.window.isVisible())

    def test_corrupt_and_invisible_saved_positions_recover(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=DESKTOP_ROOT / 'build') as folder:
            root = Path(folder)
            self.window.persist = True
            for raw in ('null', '[]', '{"position":[999999,999999]}', '{"position":[1e100,0]}'):
                (root / 'runtime-state.json').write_text(raw)
                with patch('chunxi.window.RUNTIME_ROOT', root):
                    self.window._restore_position()
                self.assertTrue(any(screen.availableGeometry().intersects(self.window.geometry()) for screen in self.app.screens()))
            self.window.persist = False

    def test_size_preview_cancel_restores_without_saving(self):
        before = copy.deepcopy(self.window.config)
        anchor = self.window.geometry().bottomLeft()
        position = self.window.pos()
        preview = []
        def adjust():
            dialog = next(w for w in self.app.topLevelWidgets() if isinstance(w, SizeDialog))
            dialog.size.slider.setValue(175)
            preview.append((self.window.width(), self.window.geometry().bottomLeft().y()))
            dialog.reject()
        QTimer.singleShot(0, adjust)
        with patch('chunxi.window.save_config') as save:
            self.window.open_size()
            save.assert_not_called()
        self.assertEqual(self.window.config, before)
        self.assertEqual(self.window.pos(), position)
        self.assertEqual(preview, [(336, anchor.y())])
        self.assertEqual(self.window.width(), round(192 * before['window']['scale']))

    def test_size_save_changes_only_scale_without_startup_write(self):
        before = copy.deepcopy(self.window.config)
        preview = []
        def adjust():
            dialog = next(w for w in self.app.topLevelWidgets() if isinstance(w, SizeDialog))
            dialog.size.slider.setValue(250)
            preview.append(dialog.size.value())
            dialog.accept()
        QTimer.singleShot(0, adjust)
        with patch('chunxi.window.save_config') as save, patch('chunxi.window.startup.set_enabled') as startup:
            self.window.open_size()
            save.assert_called_once()
            startup.assert_not_called()
        before['window']['scale'] = 2.5
        self.assertEqual(preview, [250])
        self.assertEqual(self.window.config, before)
        self.assertEqual(self.window.width(), 480)


if __name__ == "__main__":
    unittest.main(verbosity=2)
