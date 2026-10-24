# 使用与运行指南 / User and running guide

[中文主页](../README.md) · [English README](../README.en.md) · [配置 / Configuration](CONFIGURATION.md)

## 下载、启动与退出 / Download, start and exit

从 [v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) 下载 `ChunxiDesktopPet-v0.1.1-win-x64.zip` 和 `SHA256SUMS.txt`，按 [校验指南](CHECKSUMS.md) 核对后完整解压。退出旧春喜，再双击 `ChunxiDesktopPet.exe`。保留 `_internal/` 和所有附带文件。GitHub 的 Source code 是源码，不是 Windows 程序包。右键宠物或托盘图标 →“退出春喜”可正常退出并保存位置。再次启动同一程序会提示已有实例。

Download `ChunxiDesktopPet-v0.1.1-win-x64.zip` and `SHA256SUMS.txt` from the [v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1), verify using the [checksum guide](CHECKSUMS.md), and extract the entire package. Exit an older instance, then run `ChunxiDesktopPet.exe`. Keep `_internal/` and the accompanying files. GitHub's Source code downloads are not Windows app packages. Right-click the cat or tray icon and select **退出春喜** to exit and save position. Starting a second instance shows an already-running notice.

## 原始发行包与当前源码 / Original package and current source

下载包实际 EXE 是较早构建：大小在“设置…”里用 50%–200% 数值框；“暂停自动行为”是勾选暂停、取消勾选恢复；没有“调节大小…”、“打开当前配置文件”或“配置参数说明”。这些便捷入口、50%–300% 滑块与容错备份在当前源码中。原始包的非法配置可能阻止启动，请先手动备份再编辑。下方菜单翻译覆盖当前源码，下载用户应按此差异表使用，而不是寻找不存在的按钮。

The actual Release EXE is an earlier build: size is a 50%–200% numeric field under Settings; the pause action is a checkbox (check to pause, uncheck to resume). It has no Adjust size, Open active configuration or Configuration help menu. Those convenience controls, the 50%–300% slider and safe recovery/backups belong to current source. Invalid configuration can prevent the original build from starting; back up manually before edits. The translations below cover current source, so package users should follow this distinction rather than look for absent buttons.

## 菜单中英对照 / Menu translation

现有界面使用中文；下面是说明翻译，不代表已加入英文界面。
The existing UI uses Chinese; these translations document it rather than adding an English UI.

| 实际文案 / Actual label | English meaning | 操作 / Action |
|---|---|---|
| 调节大小… | Adjust size | 50%–300%，预览后保存或取消 / Preview, then Save or Cancel |
| 设置… | Settings | 大小、置顶、频率、登录启动 / Size, topmost, frequency, login startup |
| 宠物大小 / 始终置顶 | Pet size / Always on top | 显示大小与窗口层级 / Appearance size and window stacking |
| 更安静 / 默认 / 稍多一些 | Quiet / Normal / A little more | 自动动作间隔档位 / Automatic-action timing presets |
| 登录 Windows 后启动春喜 | Start Chunxi after Windows login | 勾选并保存才启用 / Enabled only after selecting and saving |
| 保存 / 取消 | Save / Cancel | 保存设置或放弃更改 / Keep or discard changes |
| 暂停自动行为 | Pause automatic behaviors | 暂停状态调度，动画仍可继续 / Pause scheduling, not necessarily the current animation |
| 恢复自动行为（当前已暂停） | Resume automatic behaviors (currently paused) | 返回坐姿，重新计时 / Return to sitting and restart timers |
| 回到屏幕右下方 | Return to the lower-right corner | 找回可见位置 / Restore a visible position |
| 打开当前配置文件 | Open active configuration | 打开实际使用的 JSON / Open the JSON actually in use |
| 配置参数说明 | Configuration help | 查看参数解释 / Read parameter help |
| 打开日志文件夹 | Open log folder | 排查问题，分享前脱敏 / Diagnose issues; sanitize before sharing |
| 退出春喜 | Exit Chunxi | 正常关闭并保存位置 / Close normally and remember position |

## 日常行为与位置 / Everyday behavior and position

启动后默认坐姿。轻微呼吸、眨眼与耳抖不是持续快速循环；空闲后卧着观察，再进入打盹。鼠标或键盘输入时间戳变化可触发缓慢唤醒；不记录输入内容。点击不保证回应，观察在鼠标进入附近区域时以概率触发。拖拽超过阈值后只移动宠物，不再当作点击。暂停后仍可拖拽和退出。

Chunxi starts sitting. Breathing, blinks and ear twitches are quiet rather than continuously busy. After inactivity, Chunxi rests and watches, then naps. Mouse movement or a changed keyboard/input timestamp can trigger a gradual wake-up; typed content is not recorded. Clicks do not guarantee a response. Observation is probabilistic when the pointer enters the nearby area. Movement past the drag threshold becomes a drag instead of a click. Dragging and exit remain available while paused.

正常退出会记住位置；显示器变化后程序尝试把窗口放回可见区域。找不到春喜时从托盘选择“回到屏幕右下方”。置顶不保证覆盖安全桌面或独占全屏。移动文件夹后重新保存登录启动设置。

Position is remembered on normal exit. Screen-layout changes trigger an attempt to keep the window visible. If Chunxi is missing, use **回到屏幕右下方** in the tray menu. Always-on-top does not override secure desktops or exclusive fullscreen. Save login-startup settings again after moving the program folder.

## 修改设置与排错 / Settings and troubleshooting

用“调节大小…”或“设置…”修改常用选项。高级时间、概率等见 [行为配置](CONFIGURATION.md)。手动改 JSON 后重启；不要拿源码模板覆盖个人配置。配置恢复提示表示安全值已应用，原文件应先备份。备份失败时不要认为已成功保存。日志可能包含本机路径，提交 Issue 前请遮盖。

Use **调节大小…** or **设置…** for common options. See [behavior configuration](CONFIGURATION.md) for intervals and probabilities. Restart after editing JSON; do not replace personal settings with a source template. A recovery notice means safe values were applied, with the original backed up first where possible. A failed backup/save is not a successful persistent update. Logs can include local paths; redact them before filing an issue.

源码启动器显示 `Please run setup.ps1 first.` 时，先按 [源码说明](../desktop/README.md) 安装环境。`Ready. Double-click Start-Chunxi.cmd.` 表示依赖安装完成。`Python virtual environment creation failed` / `Dependency installation failed` 分别表示虚拟环境或依赖安装失败，请保留完整错误供排查。程序本身的菜单和错误提示尚未全面本地化。

If the source launcher says `Please run setup.ps1 first.`, follow the [source instructions](../desktop/README.md). `Ready. Double-click Start-Chunxi.cmd.` means dependencies are installed. `Python virtual environment creation failed` and `Dependency installation failed` identify environment/dependency setup failures; retain the error for diagnosis. Application menus and error messages are not fully localized.

反馈入口：[GitHub Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues)。附版本、使用 Release 或源码、Windows 与屏幕缩放、复现步骤；不要公开个人配置原件或含隐私的日志。安全提示见 [Windows 说明](SECURITY-AND-WINDOWS.md)。

Feedback: [GitHub Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues). Include version, Release/source origin, Windows/display scale, and reproduction steps. Do not publish raw personal configuration or private logs. See [Windows security notes](SECURITY-AND-WINDOWS.md).
