"""Per-process Qt DPI smoke check. Does not change Windows display settings."""
import json,os,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QPoint,Qt
from PySide6.QtTest import QTest
from chunxi.config import DESKTOP_ROOT,load_config
from chunxi.window import PetWindow
from chunxi.settings import SettingsDialog

app=QApplication([])
config=load_config(DESKTOP_ROOT/'config/default.json')
window=PetWindow(config,persist=False)
window.show();QTest.qWait(200)
screens=[];placements=[]
for screen in app.screens():
    rect=screen.availableGeometry()
    screens.append({'name':screen.name(),'geometry':[rect.x(),rect.y(),rect.width(),rect.height()],'logical_dpi':screen.logicalDotsPerInch(),'device_pixel_ratio':screen.devicePixelRatio()})
    window.move(rect.center()-QPoint(window.width()//2,window.height()//2))
    QTest.qWait(200)
    placements.append({'target':screen.name(),'actual':window.windowHandle().screen().name(),'visible':rect.contains(window.geometry())})
root=Path(os.environ.get('CHUNXI_QA_DIR', str(DESKTOP_ROOT/'build/qa/v0.1.1')));root.mkdir(parents=True,exist_ok=True)
factor=os.environ.get('QT_SCALE_FACTOR','native')
pixmap=window.grab();pixmap.save(str(root/f'dpi-{factor}.png'))
result={'qt_process_scale_override':factor,'windows_settings_changed':False,'os_reported_mixed_dpi_test':factor=='native' and len({s['device_pixel_ratio'] for s in screens})>1,'screens':screens,'placements':placements,'logical_size':[window.width(),window.height()],'grab_pixel_size':[pixmap.width(),pixmap.height()],'pixmap_dpr':pixmap.devicePixelRatio(),'ok':all(p['actual']==p['target'] and p['visible'] for p in placements)}
(root/f'dpi-{factor}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if factor=='native':
    dialog=SettingsDialog(config,False,window);dialog.show();QTest.qWait(200)
    dialog.grab().save(str(root/'settings.png'));dialog.close()
window.close()
print(json.dumps(result))
