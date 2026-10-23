"""Run the real Windows Qt window with accelerated idle thresholds, then exit.

This is a test driver, not an alternate renderer. Screenshots use QWidget.grab().
"""
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from PySide6.QtCore import QPoint, QTimer, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from chunxi.config import DESKTOP_ROOT, load_config
from chunxi.window import PetWindow
from chunxi.state_machine import State

app=QApplication([])
config=load_config(DESKTOP_ROOT/'config/default.json')
config['behavior']['loaf_after_seconds']=[2,2]
config['behavior']['sleep_after_seconds']=[5,5]
config['behavior']['blink_interval_seconds']=[20,20]
window=PetWindow(config,persist=False,rng=random.Random(13))

class ScriptMonitor:
    active=False
    def poll(self):
        active=self.active
        self.active=False
        return active,QPoint(-10000,-10000)
monitor=ScriptMonitor()
window.monitor=monitor
window.show()
out=Path(os.environ.get('CHUNXI_QA_DIR', str(DESKTOP_ROOT/'build/qa')))
out.mkdir(parents=True,exist_ok=True)
result={'scope':'Real Windows Qt window, accelerated test clock thresholds and injected mouse-activity sample; production uses native GetLastInputInfo and QCursor.', 'states':[], 'errors':[]}
timings=[]
last=[time.monotonic()]
frame_probe=QTimer()
def probe():
    now=time.monotonic()
    timings.append((now-last[0])*1000)
    last[0]=now
frame_probe.timeout.connect(probe)
frame_probe.start(33)

def capture(label,expected):
    try:
        assert window.machine.state==expected,(label,window.machine.state)
        assert window.grab().save(str(out/f'{label}.png'))
        result['states'].append({'label':label,'state':window.machine.state.value})
    except Exception as e:
        result['errors'].append(repr(e))

def flags():
    try:
        u=ctypes.WinDLL('user32',use_last_error=True)
        u.GetWindowLongW.argtypes=[wintypes.HWND,ctypes.c_int]
        u.GetWindowLongW.restype=ctypes.c_long
        style=u.GetWindowLongW(int(window.winId()),-20)
        result['native_topmost']=bool(style&0x8)
        result['native_layered']=bool(style&0x80000)
        result['qt_translucent']=window.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        result['transparent_corner_alpha']=window.render_frame(time.monotonic()).pixelColor(0,0).alpha()
        assert result['native_topmost'] and result['native_layered'] and result['qt_translucent']
    except Exception as e:
        result['errors'].append(repr(e))

def drag():
    try:
        before=window.pos()
        QTest.mousePress(window,Qt.MouseButton.LeftButton,pos=QPoint(96,145))
        QTest.mouseMove(window,QPoint(126,155))
        QTest.mouseRelease(window,Qt.MouseButton.LeftButton,pos=QPoint(126,155))
        result['drag_moved_window']=window.pos()!=before
        result['drag_did_not_click']=window.machine.action is None
        assert result['drag_moved_window'] and result['drag_did_not_click']
    except Exception as e:
        result['errors'].append(repr(e))

def wake():
    monitor.active=True

def finish():
    frame_probe.stop()
    result['timer_samples']=len(timings)
    result['timer_max_ms']=round(max(timings),2)
    result['timer_p95_ms']=round(sorted(timings)[int(len(timings)*.95)],2)
    result['ok']=not result['errors']
    (out/'windows-runtime.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    window.close()

QTimer.singleShot(350,flags)
QTimer.singleShot(650,lambda:capture('01-sitting',State.SITTING))
QTimer.singleShot(2900,lambda:capture('02-loaf',State.LOAF))
QTimer.singleShot(5800,lambda:capture('03-sleeping',State.SLEEPING))
QTimer.singleShot(6200,wake)
QTimer.singleShot(7300,lambda:capture('04-waking',State.WAKING))
QTimer.singleShot(8700,lambda:capture('05-awake',State.SITTING))
QTimer.singleShot(8900,drag)
QTimer.singleShot(9500,finish)
sys.exit(app.exec())
