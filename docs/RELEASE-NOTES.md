## 春喜 Chunxi Desktop Pet v0.1.1

一只安静、懒洋洋的像素奶牛猫，独立生活在 Windows 桌面。正常运行不依赖 ChatGPT/Codex，也不需要联网。

### 功能

- 透明、无边框窗口，可置顶、拖拽并记住位置。
- 轻微呼吸、随机眨眼和耳朵动作；空闲后卧着观察、打盹，检测到输入活动后缓慢醒来。
- 鼠标观察、点击眨眼或轻抬爪带概率和冷却，不保证每次回应。
- 托盘/右键菜单：设置（含大小）、暂停勾选、位置恢复、日志和退出。勾选暂停、取消勾选恢复自动行为。登录启动默认关闭。

### 下载与启动

1. 在下方 Assets 下载 **[ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip)** 和 **[SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)**。
2. 用 PowerShell `Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256` 核对校验文件中同名行。
3. 完整解压，退出旧春喜，再双击 `ChunxiDesktopPet.exe`。保留 `_internal/` 及附带文件；无需安装 Python 或管理员权限。
4. **Source code (zip/tar.gz) 是源码，不是 Windows 程序包。** 校验文件中其他历史文件名不代表它们都已单独上传；不要把历史源码包哈希用于 GitHub 自动源码归档。

### 设置与已知限制

原始下载包的配置通常位于 `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`；设置里的大小数值框为 50%–200%，JSON 基础校验接受 0.8（80%）。原包没有后来新增的大小滑块、配置/帮助菜单和安全恢复备份；非法配置可能阻止启动，编辑前手动备份。界面主要是中文，[双语使用指南](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/USER-GUIDE.md) 提供翻译。

EXE 未签名，SmartScreen 可能提示。未穷尽不同硬件、DPI、热插拔、睡眠恢复、远程桌面及实际登录启动；没有因发布而宣称新耐久、Defender 或干净机器验收通过。姿态为离散帧，非整数缩放可能有像素阶梯。参见 [已知问题](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/KNOWN-ISSUES.md)。

### 版本与授权

当前 main 和 README 演示包含发布后的文档与打盹轮廓修补；本 Release 的原始 Windows 附件保持不变。源码与演示不代表附件已被更新。

程序代码采用 MIT；角色设计、像素图、动画、图标等美术不自动纳入 MIT。用户可以下载、安装和使用官方桌宠程序；美术素材不得未经许可单独提取、转载、修改、重新打包或用于商业产品。不添加 CC 或其他美术许可。第三方依赖遵循各自条款。

### 反馈

通过 [Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues) 提供版本、Windows/DPI、复现步骤和脱敏截图；不要公开私人配置或日志。[主页](https://github.com/WilliamZXT/Chunxi-Desktop-Pet) · [校验说明](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/CHECKSUMS.md) · [安全说明](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/SECURITY-AND-WINDOWS.md)

---

## Chunxi Desktop Pet v0.1.1 — English

A quiet, relaxed pixel-art tuxedo cat living independently on your Windows desktop. Normal operation requires neither ChatGPT/Codex nor an internet connection.

### Features

- Transparent, borderless window with optional topmost behavior, dragging, and position memory.
- Gentle breathing, randomized blinks and ear movements; resting and watching, then napping after inactivity; gradual wake-up on input activity.
- Pointer observation and click blinks/paw lifts use candidate probabilities and cooldowns, not guaranteed responses.
- Tray/context-menu controls for Settings (including size), a pause checkbox, position reset, logs and exit. Check to pause automatic behaviors and uncheck to resume. Login startup is off by default.

### Download and start

1. In Assets below, download **[ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip)** and **[SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)**.
2. Run PowerShell `Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256` and compare the matching filename's entry.
3. Extract everything, exit an older instance, then run `ChunxiDesktopPet.exe`. Keep `_internal/` and accompanying files. Python and administrator access are not required.
4. **Source code (zip/tar.gz) is not the Windows app package.** Other historical filenames in the checksum list are not all attached separately; do not apply a historical prepared source-package hash to GitHub's automatic source archives.

### Settings and limitations

The original package normally uses `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`. Its Settings size field offers 50%–200%; basic JSON validation accepts 0.8 (80%). It lacks later size-slider, config/help menus and safe recovery/backups. Invalid configuration can prevent startup: back up manually before editing. The UI is primarily Chinese; the [bilingual guide](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/USER-GUIDE.md) provides translations.

The EXE is unsigned and SmartScreen may warn. Hardware, DPI, hotplug, sleep/resume, Remote Desktop and actual login startup are not exhaustively validated. Publication is not a new endurance, Defender or clean-machine acceptance claim. Pose changes use discrete frames, and fractional scaling can create uneven pixel steps. See [known issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/KNOWN-ISSUES.md).

### Version and licensing

Current main and README previews include post-release documentation and a napping-contour repair. The original Windows attachment in this Release is unchanged. Updated source/previews do not imply an updated attachment.

Program code uses MIT. Character designs, pixel artwork, animations and icons are excluded from MIT. Users may download, install and use the official desktop-pet application. Without permission, artwork must not be separately extracted, reposted, modified, repackaged or used in commercial products. No CC or other artwork license is added. Dependencies retain their own terms.

### Feedback

Use [Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues) with version, Windows/DPI, reproduction steps and sanitized screenshots. Do not post private configurations or logs. [Homepage](https://github.com/WilliamZXT/Chunxi-Desktop-Pet) · [Checksums](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/CHECKSUMS.md) · [Security](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/blob/main/docs/SECURITY-AND-WINDOWS.md)
