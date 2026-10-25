# 春喜 · Chunxi Desktop Pet

**[English](README.en.md) · [下载 v0.1.1](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) · [使用指南](docs/USER-GUIDE.md) · [文档索引](docs/README.md)**

春喜是一只圆脸、金黄眼睛、安静又有点高冷的像素奶牛猫。Chunxi Desktop Pet 让它以轻微呼吸、偶尔观察和打盹的方式陪你工作。它是 Python + PySide6 编写的独立 Windows 桌宠，正常运行不依赖 ChatGPT/Codex，也不需要联网。

## 动态演示

### 坐姿 · 眨眼 · 耳朵动作

![春喜坐姿、眨眼与耳朵动作](docs/media/idle-source.gif)

### 卧着观察 · Resting and watching

![春喜卧着观察](docs/media/loaf-source.gif)

### 打盹 · Napping

![春喜打盹](docs/media/dozing-source.gif)

[打盹单帧对照](docs/media/dozing-preview.png) · [全部演示与图片说明](docs/media/README.md)

这些 GIF 展示已有动画素材，不是自动行为的实时录像；播放速度不代表实际动作间隔。演示对应当前 `main`，包含发布后的打盹轮廓局部修补；**已发布的 v0.1.1 Windows 附件未被替换**，其美术细节可能与当前源码演示不同。

## 下载与启动

**当前正式版本：[v0.1.1](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1)。** Windows x64 用户下载 **[ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip)**，同时下载 **[SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)**。

1. 完整解压 ZIP，先退出旧春喜，再双击 `ChunxiDesktopPet.exe`。
2. 保留整个文件夹，尤其是 `_internal/`；不要只移动 EXE，也不要在压缩包里直接运行。
3. Windows 包包含运行依赖，无需安装 Python 或取得管理员权限。
4. GitHub 自动生成的 **Source code (zip/tar.gz)** 是源码，不是可直接运行的 Windows 包。

在下载目录打开 PowerShell，核对 Windows ZIP 对应行：

```powershell
Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256
```

输出应与同版校验文件中的对应值一致。校验文件还列有未单独上传的历史文件名，不代表这些文件都是 Release 附件，也不能用它校验持续更新的 README。详见 [SHA-256 指南](docs/CHECKSUMS.md)。包内附带文档为历史中文版本，部分说明过时；当前双语网页文档按实际构建差异说明。

EXE 尚未签名，SmartScreen 可能提示未知发布者。核对来源和校验值；若出现威胁检测或策略拦截，应停止运行并反馈，不建议关闭防护。见 [Windows 安全说明](docs/SECURITY-AND-WINDOWS.md)。

## 当前源码与发行包的区别

本次核对了实际下载的 Windows 包。其 EXE SHA-256 为 `078c10350ad8c356bd3a7b34b16fa2421fe1806c9c8ce406e1756aaa6a32d1b8`，不是后来本机修整构建。**默认值相同不代表功能版本完全相同。**

| 项目 | 已发布 v0.1.1 Windows 包 | 当前 main |
|---|---|---|
| 大小界面 | “设置…”内 50%–200% 数值框 | “调节大小…”滑块与设置，50%–300% |
| 配置入口 | 无专用打开配置/参数帮助菜单 | 有打开配置与参数说明菜单 |
| 暂停/恢复 | 勾选“暂停自动行为”暂停，取消勾选恢复 | 显示明确的暂停/恢复状态文案 |
| 配置容错 | 有基础范围校验；非法 JSON/越界可能阻止启动，不具备后来安全恢复与备份实现 | 按字段校验、安全修正、提示和修复前备份 |
| 打盹美术 | 原始发行素材 | 已确认左侧轮廓修补 |

下方高级菜单与容错描述以当前源码为准。下载用户修改 JSON 前应先手动备份；不要以为原发行包会自动修复错误。本轮不更换附件，完整说明见 [使用指南](docs/USER-GUIDE.md)。

标签来源补充：`v0.1.1` 标签指向 `453b74cf836b8de45056b32fbd7f3403bcba542f`，其应用源码与当前 main 相同，含原始 Windows 附件没有的后续功能，因此 GitHub 自动标签源码包不能视为该 EXE 的精确构建输入。本地历史源码归档（SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`）的 11 个应用模块、启动入口与内嵌代码静态一致，9 项随包资源字节一致；该归档尚未公开附加，精确历史 Git 提交与可重复二进制构建未建立。

## 功能与操作

- 透明、无边框窗口；可置顶、拖拽，退出时记住位置，屏幕布局改变时尽量保持可见。
- 坐姿轻微呼吸、随机眨眼与耳抖；空闲后卧着观察、打盹，检测到输入活动后缓慢醒来。
- 鼠标进入附近范围时偶尔观察；点击有概率眨眼或轻抬爪，并有冷却。拖拽不会同时触发点击。
- 右键春喜或托盘图标打开菜单。界面目前以中文显示，英文对照见 [使用指南](docs/USER-GUIDE.md)。

以下菜单清单为当前源码；原发行包仅包含其中的设置、暂停勾选、位置恢复、日志和退出。

| 菜单 | 用途 |
|---|---|
| 调节大小… | 50%–300% 实时预览；保存记住，取消恢复 |
| 设置… | 大小、始终置顶、行为频率、可选登录启动 |
| 暂停自动行为 / 恢复自动行为（当前已暂停） | 暂停或恢复调度；当前动画仍可播放 |
| 回到屏幕右下方 | 找回位置 |
| 打开当前配置文件 / 配置参数说明 | 编辑实际配置或查看参数解释 |
| 打开日志文件夹 | 获取排错记录，分享前移除个人路径 |
| 退出春喜 | 正常关闭桌宠 |

登录启动默认关闭，只在勾选并保存后启用；移动程序后需重新保存启动设置。桌宠不包含 AI 对话、语音、重力或窗口边缘停留。

## 自动行为与行为配置

以下为 [默认配置](desktop/config/default.json)，并非你的个人设置。`normal` 频率下：

| 行为 | 默认条件 |
|---|---|
| 眨眼 / 耳抖 | 随机间隔 12–28 / 65–145 秒；受当前状态与其他动作影响 |
| 卧着观察 / 打盹 | 总空闲时间达到随机阈值 50–95 / 210–330 秒 |
| 醒来 | 检测到输入活动后约 1.5 秒 |
| 鼠标观察 | 进入附近范围时有 22% 候选概率，冷却 45–100 秒 |
| 点击互动 | 有 40% 候选概率，冷却 30–70 秒；部分重复反馈会跳过 |

默认大小 `scale=1.0`；支持 `0.5–3.0`，`0.8` 是合法的 80% 大小。设置可选更安静、默认、稍多一些；行为频率不是“每次输入必定回应”。

EXE 默认配置：`%LOCALAPPDATA%/ChunxiDesktopPet/config.json`；源码默认配置：`desktop/build/config.json`。`--config PATH` 指定实际使用的文件。运行环境可能重定向用户目录，以“打开当前配置文件”为准。有效用户值优先，升级不应拿默认模板覆盖个人设置。手动编辑后重启；界面保存立即生效。备份文件不会自动清理。

大小、时间区间、概率、靠近半径、鼠标/拖拽阈值等完整说明与安全恢复规则见 [行为配置](docs/CONFIGURATION.md)。位置另外保存于运行目录下的 `runtime-state.json`，正常退出时写入。

## 从源码运行与构建

Windows x64、Python 3.12。从 `desktop/` 目录执行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\run.py
```

也可先运行 `setup.ps1`，再双击 `Start-Chunxi.cmd`。迁移源码后重建虚拟环境。PySide6 固定为 6.10.0。构建使用 PyInstaller 6.16.0 与 hooks 2026.9：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\build\build.ps1
```

输出 `desktop/build/dist/v0.1.1/ChunxiDesktopPet/`，必须完整分发文件夹。详见 [开发与运行说明](desktop/README.md)。

## 目录与文档

`desktop/` 为独立桌宠，`shared/sprites/` 为像素资源，`lite/` 保留原宿主宠物快照；Lite 不参与独立程序运行。文档入口：[使用](docs/USER-GUIDE.md)、[配置](docs/CONFIGURATION.md)、[已知问题](docs/KNOWN-ISSUES.md)、[安全](docs/SECURITY-AND-WINDOWS.md)、[检查范围](docs/TEST-REPORT.md)、[发布说明](docs/RELEASE-NOTES.md)、[更新记录](CHANGELOG.md)。

## 已知限制与反馈

姿态切换为离散帧；非整数缩放可能出现不等宽像素阶梯。尚未穷尽硬件热插拔、睡眠恢复、远程桌面和实际登录启动等环境。没有为本轮文档整理重跑运行或耐久测试；请区分历史验证与本轮链接/文档检查，见 [检查摘要](docs/TEST-REPORT.md)。

通过 [GitHub Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues) 反馈，附版本、Windows 版本、缩放比例、复现步骤和脱敏截图/日志；说明使用的是 Release 包还是当前源码。敏感安全问题先看 [SECURITY.md](SECURITY.md)。后续事项以已知问题和更新记录为准，目前没有承诺的新版本时间表。

## 授权

程序源码、测试及构建/启动脚本采用 [MIT License](LICENSE-CODE-MIT.txt)。春喜的角色设计、像素图、动画、图标、图集及其他美术素材不自动纳入 MIT，保留美术版权。用户可以下载、安装和使用官方桌宠程序；未经许可，美术素材不得单独提取、转载、修改、重新打包或用于商业产品。不添加 CC 或其他美术许可证。

第三方组件遵循各自许可证，Windows 包内声明见 `THIRD-PARTY-NOTICES/`。详见 [授权边界](docs/LICENSE-OPTIONS.md)。
