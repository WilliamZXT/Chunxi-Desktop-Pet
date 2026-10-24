# 已知问题与限制 / Known issues and limitations

[使用 / Use](USER-GUIDE.md) · [检查范围 / Validation scope](TEST-REPORT.md)

## 当前限制 / Current limitations

| 中文 | English |
|---|---|
| EXE 未签名，SmartScreen 可能提示。没有对当前下载包提供新的 Defender 或真实下载信誉验收结论。 | The EXE is unsigned and may trigger SmartScreen. No new Defender or real-download reputation acceptance is claimed for the current package. |
| 姿态采用完整离散帧切换，没有坐下/起身中间素材；非整数缩放可能产生不等宽像素阶梯。 | Poses change using discrete full frames, without intermediate sit/stand artwork. Fractional scaling may produce uneven pixel steps. |
| 物理热插拔、睡眠恢复、远程桌面、不同显卡和所有 DPI 组合未穷尽测试。置顶可能被安全桌面或独占全屏覆盖。 | Physical hotplug, sleep/resume, Remote Desktop, GPUs and all DPI combinations are not exhaustively tested. Secure desktops or exclusive fullscreen can cover the pet. |
| 登录启动登记逻辑有检查记录，但尚无实际注销/登录验收。移动程序后需重新保存该设置。 | Login-startup registration has check records, but actual sign-out/sign-in acceptance is not established. Save the setting again after moving the program. |
| 不声称发布后的打盹美术修补做过新的两小时耐久或独立干净电脑验收。 | Post-release napping-art repairs have no new two-hour endurance or independent clean-machine acceptance claim. |
| 原始 Release EXE 早于当前 main：设置大小为 50%–200%，缺少后续滑块、打开配置/帮助入口与安全恢复备份；非法配置可能阻止该旧构建启动。 | The original Release EXE predates current main: Settings exposes 50%–200%, without the later slider, config/help menus or safe recovery/backups. Invalid configuration can prevent that earlier build from starting. |
| 现有 UI 主要为中文；使用指南提供菜单英译，不代表程序已支持英文界面。 | The current UI is primarily Chinese. The guide translates menu labels; the application is not presented as having an English UI. |
| 配置和位置可位于不同运行目录，Windows 应用容器也可能重定向目录；请从菜单打开实际配置。 | Configuration and position depend on the runtime location, and Windows containers may redirect folders. Open the active configuration from the menu. |
| 配置备份不会自动删除，日志可能含本地路径，分享前需脱敏。 | Configuration backups are not deleted automatically; logs can contain local paths and should be sanitized before sharing. |
| main 已有发布后的文档与打盹轮廓修补；原始 v0.1.1 Windows 附件保持不变。 | Main contains post-release documentation and a napping-contour repair; the original v0.1.1 Windows attachment is unchanged. |
| 校验文件包含未单独上传的历史文件名，只有 Windows ZIP 对应行用于当前 Windows 下载包。 | The checksum asset lists historical unattached filenames; use the Windows ZIP entry for the current Windows download. |

## 已修复的问题 / Resolved issues

当前源码已包含配置容错、scale 支持范围校验、拖拽/点击分离、窗口可见位置处理和打盹左侧轮廓修补；不要把这些仍写成“未实现”。修复范围与验证证据见 [更新记录](../CHANGELOG.md) 和 [检查摘要](TEST-REPORT.md)。这不意味着原始发行包自动取得后续美术修改。

Current source includes configuration recovery, supported-scale validation, drag/click separation, visible-position handling, and the napping left-contour repair. These are implemented rather than pending features. See the [changelog](../CHANGELOG.md) and [validation summary](TEST-REPORT.md) for scope and evidence. The original release package does not automatically receive later artwork changes.

AI 对话、语音、重力和窗口边缘停留不在当前功能范围；没有本轮新增功能或新版本时间表。
AI conversation, voice, gravity and window-edge perching are outside current scope. This pass adds no features or promised version schedule.
