import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from chunxi.config import ConfigRecovery, DESKTOP_ROOT, load_config, save_config, validate_config


class ConfigRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=DESKTOP_ROOT / 'build')
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'config.json'
        self.defaults = json.loads((DESKTOP_ROOT / 'config/default.json').read_text(encoding='utf-8'))

    def write(self, data):
        self.path.write_text(json.dumps(data), encoding='utf-8')
        return self.path.read_bytes()

    def test_default_and_missing_file(self):
        config = load_config(self.path)
        self.assertEqual(config, self.defaults)
        self.assertEqual(json.loads(self.path.read_text()), self.defaults)

    def test_approved_profile_and_user_override_precedence(self):
        profile = copy.deepcopy(self.defaults)
        profile['window']['scale'] = 0.75
        profile['window']['transition_ms'] = 650
        original = self.write(profile)
        config = load_config(self.path)
        self.assertEqual(config['window']['scale'], 0.75)
        self.assertEqual(config['behavior']['blink_interval_seconds'], [12, 28])
        self.assertEqual(config['behavior']['ear_interval_seconds'], [65, 145])
        self.assertEqual(config['behavior']['click_cooldown_seconds'], [30, 70])
        self.assertEqual(config['behavior']['look_probability'], 0.22)
        self.assertEqual(config['behavior']['click_probability'], 0.4)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(config['window']['transition_ms'], 650)

    def test_read_permission_failure_does_not_attempt_to_replace_user_file(self):
        original = self.write(self.defaults)
        from chunxi import config as module
        real_read = module._read_json
        def read(path):
            if path == self.path:
                raise PermissionError
            return real_read(path)
        with patch.object(module, '_read_json', side_effect=read), patch.object(module, '_atomic_write') as write:
            validate_config(load_config(self.path))
            write.assert_not_called()
        self.assertEqual(self.path.read_bytes(), original)

    def test_scale_08_is_preserved_without_rewriting_user_file(self):
        data = {'version': '0.1.0', 'window': {'scale': 0.8}, 'behavior': {'click_probability': 0.17}, 'personal_extra': 'keep'}
        original = self.write(data)
        report = ConfigRecovery()
        config = load_config(self.path, recovery=report)
        self.assertEqual(config['window']['scale'], 0.8)
        self.assertEqual(config['behavior']['click_probability'], 0.17)
        self.assertEqual(config['personal_extra'], 'keep')
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(report.issues)
        self.assertFalse(list(self.path.parent.glob('*.bak')))

    def test_scale_6_clamps_and_backs_up_original_bytes(self):
        data = copy.deepcopy(self.defaults)
        data['window']['scale'] = 6.0
        data['preferences']['frequency'] = 'quiet'
        data['behavior']['click_probability'] = 0.17
        original = self.write(data)
        report = ConfigRecovery()
        config = load_config(self.path, recovery=report)
        self.assertEqual(config['window']['scale'], 3)
        self.assertEqual(config['preferences']['frequency'], 'quiet')
        self.assertEqual(config['behavior']['click_probability'], 0.17)
        self.assertEqual(report.backup.read_bytes(), original)
        self.assertTrue(report.persisted)
        self.assertEqual(json.loads(self.path.read_text()), config)

    def test_types_ranges_and_logical_order_recover_field_by_field(self):
        data = copy.deepcopy(self.defaults)
        data['window']['scale'] = 'large'
        data['window']['always_on_top'] = 'false'
        data['behavior']['click_probability'] = 4
        data['behavior']['look_probability'] = -1
        data['behavior']['blink_interval_seconds'] = [28, 12]
        data['behavior']['ear_interval_seconds'] = 'no'
        data['behavior']['sleep_after_seconds'] = [1, 2]
        data['interaction']['poll_ms'] = 0
        data['interaction']['drag_threshold_pixels'] = False
        self.write(data)
        config = load_config(self.path)
        validate_config(config)
        self.assertEqual(config['window']['scale'], 1)
        self.assertEqual(config['behavior']['click_probability'], 1)
        self.assertEqual(config['behavior']['look_probability'], 0)
        self.assertEqual(config['behavior']['blink_interval_seconds'], [12, 28])
        self.assertEqual(config['behavior']['ear_interval_seconds'], [65, 145])
        self.assertGreater(config['behavior']['sleep_after_seconds'][0], 95)
        self.assertEqual(config['interaction']['poll_ms'], 20)
        self.assertEqual(config['interaction']['drag_threshold_pixels'], 6)

    def test_illegal_json_and_encoding_preserve_backups(self):
        for raw in (b'{"window":', b'\xff\xfe\x80', b'{"window":{"scale":NaN}}', b'[]', b'null'):
            with self.subTest(raw=raw):
                self.path.write_bytes(raw)
                report = ConfigRecovery()
                config = load_config(self.path, recovery=report)
                self.assertEqual(config, self.defaults)
                self.assertEqual(report.backup.read_bytes(), raw)
                self.assertTrue(report.issues)

    def test_wrong_sections_bool_scale_and_huge_numbers(self):
        cases = [
            {'window': None, 'interaction': []},
            {'window': {'scale': True}},
            {'window': {'scale': 10**400, 'position': [10**100, 0]}},
            {'interaction': {'poll_ms': [], 'drag_threshold_pixels': 6.0}},
            {'preferences': {'frequency': []}},
        ]
        for data in cases:
            with self.subTest(data=data):
                self.write(data)
                validate_config(load_config(self.path))

    def test_backup_failure_never_overwrites_original(self):
        original = self.write({'window': {'scale': 6}})
        report = ConfigRecovery()
        with patch('chunxi.config._backup', side_effect=PermissionError):
            config = load_config(self.path, recovery=report)
        self.assertEqual(config['window']['scale'], 3)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(report.persisted)
        self.assertTrue(report.issues)

    def test_check_mode_never_repairs_or_backs_up_on_disk(self):
        original = self.write({'window': {'scale': 6}})
        report = ConfigRecovery()
        self.assertEqual(load_config(self.path, recovery=report, repair=False)['window']['scale'], 3)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertIsNone(report.backup)

    def test_save_is_valid_atomic_and_backed_up(self):
        original = self.write(self.defaults)
        changed = copy.deepcopy(self.defaults)
        changed['window']['scale'] = 0.8
        save_config(changed, self.path)
        self.assertEqual(json.loads(self.path.read_text()), changed)
        self.assertEqual(next(self.path.parent.glob('*.bak')).read_bytes(), original)
        before = self.path.read_bytes()
        changed['window']['scale'] = 6
        with self.assertRaises(ValueError):
            save_config(changed, self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse(list(self.path.parent.glob('*.tmp')))

    def test_replace_failure_preserves_old_file_and_cleans_temporary(self):
        original = self.write(self.defaults)
        with patch.object(Path, 'replace', side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                save_config(self.defaults, self.path)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(list(self.path.parent.glob('*.tmp')))
