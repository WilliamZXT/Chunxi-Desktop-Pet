"""Native Qt size-dialog check; never writes the user's configuration or startup."""
import copy
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from chunxi.config import load_config
from chunxi.settings import SizeDialog
from chunxi.window import PetWindow

app = QApplication([])
app.setQuitOnLastWindowClosed(False)
out = Path(__file__).resolve().parents[1] / 'build/qa/size-control'
out.mkdir(parents=True, exist_ok=True)
window = PetWindow(load_config(), persist=False)
window.show()
results = []

def exercise(mode):
    before = copy.deepcopy(window.config)
    errors = []
    def interact():
        dialog = next(w for w in app.topLevelWidgets() if isinstance(w, SizeDialog) and w.isVisible())
        try:
            dialog.size.slider.setValue(150 if mode == 'cancel' else 125)
            app.processEvents()
            assert window.width() == (288 if mode == 'cancel' else 240)
            if mode == 'save':
                assert dialog.grab().save(str(out / 'size-control.png'))
                assert window.grab().save(str(out / 'pet-preview.png'))
            dialog.reject() if mode == 'cancel' else dialog.accept()
        except Exception as error:
            errors.append(str(error))
            dialog.reject()
    QTimer.singleShot(150, interact)
    with patch('chunxi.window.save_config') as save, patch('chunxi.window.startup.set_enabled') as startup:
        window.open_size()
        assert not errors, errors
        assert not startup.called
        if mode == 'cancel':
            assert window.config == before and not save.called
        else:
            expected = copy.deepcopy(before)
            expected['window']['scale'] = 1.25
            assert window.config == expected
            save.assert_called_once_with(expected, window.config_path)
    results.append(mode)

def run():
    try:
        exercise('cancel')
        exercise('save')
        result = {'ok': True, 'platform': app.platformName(), 'checks': results,
                  'config_and_registry_writes': False, 'time': time.time()}
    except Exception as error:
        result = {'ok': False, 'error': str(error), 'checks': results}
    (out / 'native-ui.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    window.close()
    app.exit(0 if result['ok'] else 1)

QTimer.singleShot(300, run)
sys.exit(app.exec())
