# 独立桌宠：运行与构建 / Desktop app: run and build

[中文主页](../README.md) · [English README](../README.en.md) · [使用指南 / User guide](../docs/USER-GUIDE.md)

## Windows 下载用户 / Windows package users

使用正式 Release 的 Windows ZIP，完整解压后运行 `ChunxiDesktopPet.exe`。不需要 Python。保留 `_internal/` 和附带文件。关闭、大小、暂停、配置与菜单翻译见使用指南；不要把 Source code 当作安装包。

Use the Windows ZIP from the published Release, extract everything, and run `ChunxiDesktopPet.exe`. Python is not required. Keep `_internal/` and accompanying files. See the user guide for exit, size, pause, configuration and menu translations. Source code archives are not application packages.

下载包 EXE 是较早构建，与当前源码的菜单、大小界面及配置恢复能力不同，详见 [使用指南](../docs/USER-GUIDE.md)。
The published EXE is an earlier build with different menus, size controls and configuration recovery; see the [user guide](../docs/USER-GUIDE.md).

## 源码运行 / Run source

要求 / Requirements: Windows x64, Python 3.12, PySide6 6.10.0. 从此 `desktop/` 目录执行 / From this `desktop/` directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\run.py
```

也可用 `setup.ps1` 安装依赖，再双击 `Start-Chunxi.cmd`。启动器缺少环境时会提示先运行 setup。源码移动目录后重建虚拟环境。需要联网的是安装依赖或下载，不是正常桌宠运行。

Alternatively, use `setup.ps1` to install dependencies, then double-click `Start-Chunxi.cmd`. The launcher asks for setup if the environment is absent. Recreate virtual environments after relocating source. Downloads and dependency installation need network access; normal pet operation does not.

源码默认配置为 `build/config.json`，EXE 默认使用用户目录；`--config PATH` 可指定文件。不要把真实个人配置复制到默认模板，详见 [配置](../docs/CONFIGURATION.md)。

Source runs default to `build/config.json`; EXE runs normally use the user directory. `--config PATH` selects a file. Do not copy personal settings into the factory template. See [configuration](../docs/CONFIGURATION.md).

## 构建 / Build

构建依赖固定在 `requirements-build.txt`；从 `desktop/` 执行 / Build dependencies are pinned in `requirements-build.txt`; run from `desktop/`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\build\build.ps1
```

输出 `build/dist/v0.1.1/ChunxiDesktopPet/`。`-Variant NAME` 输出到 `v0.1.1-NAME`，用于避免覆盖另一份工作副本；构建脚本不会替你发布 Release。保持完整 onedir 目录和第三方声明，不只复制 EXE。构建会隔离外部 PATH，避免无关原生 DLL 混入。

Output is `build/dist/v0.1.1/ChunxiDesktopPet/`. `-Variant NAME` selects `v0.1.1-NAME`, allowing a separate working copy. Building does not publish a Release. Keep the complete onedir distribution and third-party notices, not only the EXE. The build isolates external PATH entries to avoid unrelated native DLLs.

## 验证与代码结构 / Validation and layout

```powershell
.\.venv\Scripts\python.exe .\run.py --check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`--check` 加载配置和资源但不打开常驻桌宠，不等同于真实 GUI 或硬件验收。当前文档整理未重新构建或重跑这些命令。`src/chunxi/` 分为窗口、动画、状态机、交互、配置、设置、启动与显示处理；`assets/`、`config/`、`tests/`、`build/` 分别保存资源映射、默认模板、检查和构建工具。`shared/sprites/` 位于项目根目录。

`--check` loads configuration and resources without opening a persistent pet; it is not full GUI or hardware acceptance. This documentation pass does not rebuild or rerun these commands. `src/chunxi/` separates window, animation, state-machine, interaction, configuration, settings, startup and display logic. `assets/`, `config/`, `tests/` and `build/` hold mappings, defaults, checks and build tools. `shared/sprites/` lives at the project root.

代码与美术授权分开，见 [授权边界 / Licensing boundaries](../docs/LICENSE-OPTIONS.md)。
