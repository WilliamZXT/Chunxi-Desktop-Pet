"""Add run instructions and the dependency license files shipped by vendors."""
from pathlib import Path
import shutil
import sys
import argparse

desktop=Path(__file__).resolve().parents[1]
version=(desktop/'VERSION').read_text().strip()
parser = argparse.ArgumentParser()
parser.add_argument('--destination', type=Path)
args = parser.parse_args()
destination=args.destination or desktop/f'build/dist/v{version}/ChunxiDesktopPet'
site=desktop/'.venv/Lib/site-packages'
notices=destination/'THIRD-PARTY-NOTICES'
notices.mkdir(exist_ok=True)
for pattern in ('pyside6-*.dist-info','pyside6_essentials-*.dist-info','pyside6_addons-*.dist-info','shiboken6-*.dist-info','pyinstaller-*.dist-info'):
    for info in site.glob(pattern):
        folder=notices/info.name
        folder.mkdir(exist_ok=True)
        for name in ('METADATA','licenses'):
            source=info/name
            if source.is_dir(): shutil.copytree(source,folder/name,dirs_exist_ok=True)
            elif source.exists(): shutil.copy2(source,folder/name)
for name in ('LICENSE.txt','LICENSE'):
    source=Path(sys.base_prefix)/name
    if source.exists(): shutil.copy2(source,notices/('Python-'+name))
(destination/'使用说明.txt').write_text(
    f'春喜 Desktop Pet v{version}\n\n双击 ChunxiDesktopPet.exe。保留整个文件夹，不能单独移动 EXE。\n'
    '右键春喜或托盘图标，选择“退出春喜”即可关闭。\n'
    '眨眼12–28秒、耳抖65–145秒；无输入50–95秒卧着观察，总空闲210–330秒打盹。\n'
    '移动鼠标/键盘输入会缓慢醒来；单击和靠近反应带概率与冷却，不一定回应。\n'
    '拖拽移动；没有重力、边缘停留、语音或AI对话。\n'
    '右键菜单“设置…”支持大小、置顶、行为频率、开机启动（默认关闭）。\n'
    '右键“调节大小…”可拖动滑块实时预览50%–300%，保存记住、取消恢复。\n'
    '配置和日志：%LOCALAPPDATA%\\ChunxiDesktopPet\\。从界面保存立即生效。\n'
    '本程序复用已确认像素素材。第三方依赖声明见 THIRD-PARTY-NOTICES。\n\n'
    'English — Chunxi Desktop Pet v' + version + '\n\n'
    'Run ChunxiDesktopPet.exe after extracting the entire folder; keep _internal/.\n'
    'Right-click the cat or tray icon: Exit Chunxi = 退出春喜; Pause automatic behaviors = 暂停自动行为; Resume = 恢复自动行为.\n'
    'Default blinks: 12–28s; ears: 65–145s; resting and watching after 50–95s idle; napping after 210–330s total idle.\n'
    'Input activity wakes Chunxi gradually. Click and proximity reactions are probabilistic and have cooldowns. Drag to move.\n'
    'Adjust size = 调节大小… (50%–300%); Settings = 设置… (size, topmost, frequency, optional login startup, off by default).\n'
    'Config/logs: %LOCALAPPDATA%/ChunxiDesktopPet/; open the active config from the menu. UI saves apply immediately.\n'
    'No gravity, edge perching, voice or AI conversation. See repository USER-GUIDE and licensing notes.\n'
    'Code uses MIT; character art is excluded. Official application use is allowed; separate artwork extraction, reposting, modification, repackaging or commercial use requires permission.\n'
    '第三方组件遵循各自条款。代码 MIT 不包含美术；官方程序可下载使用，美术单独提取、转载、修改、重新打包或商用需许可。\n',encoding='utf-8')
print('Distribution instructions and vendor notices saved.')
