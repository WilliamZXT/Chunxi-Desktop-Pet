## 春喜 Chunxi Desktop Pet v0.1.1

一只安静、懒洋洋的像素奶牛猫，独立陪伴在 Windows 桌面。正常运行无需 ChatGPT/Codex、Python 安装或联网。

### 功能

- 透明无边框窗口，可置顶、拖拽并记住位置。
- 轻微呼吸、随机眨眼与耳朵动作；空闲后卧着观察、打盹，输入活动后缓慢醒来。
- 鼠标观察和点击反应有概率与冷却，不保证每次回应。
- “设置…”提供 50%–200% 大小数值框、置顶、行为频率和可选登录启动；登录启动默认关闭。
- 勾选“暂停自动行为”暂停，取消勾选恢复；右键菜单还可恢复位置、打开日志和退出。

### 下载、校验与启动

1. 下载 [ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip) 与 [SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)。
2. 在 PowerShell 执行 `Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256`，与校验文件同名行比对。Windows ZIP 的 SHA-256：

```text
8f1cc6d990ff135374f92036097f86023639ddad5662e08c3ec862a3e6869c01
```

3. 完整解压，退出旧春喜，再运行 `ChunxiDesktopPet.exe`。保留 `_internal/` 及附带文件，不要只移动 EXE。
4. GitHub 自动生成的 **Source code (zip/tar.gz)** 是标签源码，不是 Windows 程序包。校验清单还包含未单独上传的历史文件名；不要将历史源码包哈希用于 GitHub 自动源码归档。

### 源码与构建对应关系

**本 Release 的标签源码并非该 Windows ZIP 的精确构建输入。** `v0.1.1` 标签指向 `453b74cf836b8de45056b32fbd7f3403bcba542f`，已含后续滑块、配置入口及安全恢复代码；这些功能不在本页原始 Windows 附件中。

已找到与 EXE 内嵌应用代码静态一致的本地历史归档 `chunxi-pet-v0.1.1-source.zip`（SHA-256：`a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`），但它尚未作为本 Release 的独立附件提供。未建立该历史快照的精确 Git 提交或可重复构建证明。当前 main 的菜单、恢复能力及修补后的打盹素材也不应自动归于此下载包。

### 设置与限制

配置通常位于 `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`。基础大小校验接受 `0.8`（80%），但原包没有后来加入的大小滑块、配置/帮助入口及安全恢复备份；非法 JSON 或越界值可能阻止启动，手动编辑前请先备份。

EXE 未签名，SmartScreen 可能提示。硬件热插拔、睡眠恢复、远程桌面、所有 DPI 组合及实际登录启动未穷尽验证。历史本机记录包含相同 EXE 的两小时运行完成结果；本次一致性审查只做静态核对，没有重跑程序、耐久或安全扫描，不将历史结果作为所有环境的保证。

### 授权与反馈

程序代码使用 MIT。角色设计、像素图、动画和图标等美术不自动纳入 MIT。用户可以下载、安装和使用官方桌宠程序；未经许可，美术不得单独提取、转载、修改、重新打包或用于商业产品。不添加 CC 或其他美术许可。第三方组件遵循各自条款。

[中文主页](https://github.com/WilliamZXT/Chunxi-Desktop-Pet) · [English README](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/README.en.md) · [双语使用指南](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/USER-GUIDE.md) · [问题反馈](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues)

反馈请附版本、Windows/DPI、复现步骤及脱敏截图，说明使用 Release 包还是当前源码；不要公开私人配置、令牌或原始日志。

---

## Chunxi Desktop Pet v0.1.1 — English

A quiet, relaxed pixel-art tuxedo cat for your Windows desktop. Normal operation requires neither ChatGPT/Codex, a separate Python installation, nor an internet connection.

### Features

- Transparent, borderless window with optional topmost behavior, dragging and position memory.
- Gentle breathing, randomized blinks and ear movements; resting and watching, then napping after inactivity; gradual wake-up on input activity.
- Pointer observation and click reactions use probabilities and cooldowns, not guaranteed responses.
- Settings offers a 50%–200% numeric size field, topmost behavior, behavior frequency and optional login startup, off by default.
- Check **暂停自动行为** to pause automatic behaviors and uncheck it to resume. The context menu also offers position reset, logs and exit.

### Download, verify and start

1. Download [ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip) and [SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt).
2. Run `Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256` in PowerShell and compare the matching filename. Windows ZIP SHA-256:

```text
8f1cc6d990ff135374f92036097f86023639ddad5662e08c3ec862a3e6869c01
```

3. Extract everything, exit any older instance, then run `ChunxiDesktopPet.exe`. Keep `_internal/` and accompanying files; do not move the EXE alone.
4. GitHub's automatic **Source code (zip/tar.gz)** archives contain tag source, not the Windows application. The checksum list also names unattached historical files; do not apply a prepared-source hash to GitHub's automatic source archives.

### Source and build provenance

**The Release tag is not the exact source input for this Windows ZIP.** Tag `v0.1.1` points to `453b74cf836b8de45056b32fbd7f3403bcba542f`, which already contains later slider, configuration-access and safe-recovery code absent from the original Windows attachment.

A local historical archive, `chunxi-pet-v0.1.1-source.zip` (SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`), statically matches the embedded application code, but is not separately attached to this Release. Its exact historical Git commit and a reproducible binary build have not been established. Current-main menus, recovery features and repaired napping artwork must not be attributed automatically to this download.

### Settings and limitations

Configuration normally resides at `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`. Basic scale validation accepts `0.8` (80%), but the original package lacks later size-slider, config/help menus and safe recovery/backups. Invalid JSON or out-of-range values can prevent startup; back up manually before editing.

The EXE is unsigned and may trigger SmartScreen. Physical hotplug, sleep/resume, Remote Desktop, all DPI combinations and actual login startup are not exhaustively validated. Historical local records include a completed two-hour run of the same EXE. This consistency review performs static checks only, with no new app execution, endurance run or security scan; historical results are not guarantees for every environment.

### Licensing and feedback

Program code uses MIT. Character designs, pixel artwork, animations, icons and other artwork are excluded from MIT. Users may download, install and use the official desktop-pet application. Without permission, artwork must not be separately extracted, reposted, modified, repackaged or used in commercial products. No CC or other artwork license is added. Dependencies retain their own terms.

[Chinese homepage](https://github.com/WilliamZXT/Chunxi-Desktop-Pet) · [English README](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/README.en.md) · [Bilingual user guide](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/USER-GUIDE.md) · [Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues)

Include version, Windows/DPI, reproduction steps and sanitized screenshots, stating whether you used the Release package or current source. Do not post private configurations, tokens or raw logs.
