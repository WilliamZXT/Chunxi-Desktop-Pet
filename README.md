# 春喜 · Chunxi Desktop Pet

一只安静、懒洋洋、略微高冷的像素奶牛猫，默默陪你工作。基于 Python + PySide6 的独立 Windows 桌面宠物，不依赖 ChatGPT/Codex，也不需要联网。

**v0.1.1：Release 草稿准备中，尚未正式发布。** [English](README.en.md)

![春喜坐姿](docs/media/sitting.png)

## 下载与启动

发布后在本仓库的 **Releases → v0.1.1 → Assets** 下载 `ChunxiDesktopPet-v0.1.1-win-x64.zip`，并用同批 `SHA256SUMS.txt` 核对。仓库：[WilliamZXT/Chunxi-Desktop-Pet](https://github.com/WilliamZXT/Chunxi-Desktop-Pet)。[Releases](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases) 仅在正式发布后提供公开下载；草稿附件暂不可公开下载。

1. 完整解压，退出旧春喜，再双击 ChunxiDesktopPet.exe。
2. 保留整个文件夹，尤其是 _internal/。无需另装Python或管理员权限。
3. 已有用户配置继续使用，不随源码或发布包上传。新用户使用出厂默认值，可通过右键设置修改大小与行为频率。
4. 配置默认保存在 %LOCALAPPDATA%/ChunxiDesktopPet/config.json；右键“打开当前配置文件”可核对实际路径。

## 功能与操作

- 透明、无边框窗口，可置顶、拖拽移动；拖拽不会同时触发点击。
- 坐姿轻微呼吸，随机眨眼、耳抖；空闲后猫饼、打盹，活动后缓慢醒来。
- 鼠标靠近时偶尔观察；点击有概率眨眼或小幅抬爪，有冷却，部分重复反馈会跳过。
- 右键宠物或托盘 → **调节大小…**：50%–300% 实时预览，保存记住，取消恢复。
- **设置…**：大小、置顶、行为频率和可选登录启动；登录启动默认关闭。
- **暂停自动行为 / 恢复自动行为（当前已暂停）**：控制状态调度，当前动画仍可播放。
- **退出春喜**：关闭程序。**回到屏幕右下方**：找回位置。

![既有动画示例](docs/media/idle-source.gif)

GIF 为既有素材演示，不是当前状态机的长时间行为录像；本版未重新生成角色或动画。

## 默认行为

眨眼12–28秒、耳抖65–145秒；空闲50–95秒猫饼、210–330秒打盹。观察概率22%、冷却45–100秒；点击候选概率40%、冷却30–70秒。部分重复反馈会跳过。个人配置不纳入仓库和下载包，已有设置不会被默认模板覆盖。

## 源码运行与打包

Windows x64、Python 3.12，在 `desktop/` 目录执行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\run.py
```

已有环境也可双击 `Start-Chunxi.cmd`。迁移源码后重建虚拟环境，不搬运旧 `.venv`。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\build\build.ps1
```

输出：`desktop/build/dist/v0.1.1/ChunxiDesktopPet/`。完整复制该文件夹，不能只分发 EXE。构建隔离外部工具 PATH，避免错误收集原生依赖。运行依赖 PySide6 6.10.0；构建依赖 PyInstaller 6.16.0、hooks 2026.9，见依赖清单。

## 目录

```text
lite/                 原有宿主宠物快照，未改变其行为接口
 desktop/             独立 Windows 桌宠
  src/chunxi/         窗口、动画、状态机、交互、配置、设置、启动与显示处理
  assets/             动画映射、应用图标
  config/             默认配置模板
  tests/              已有自动检查与本地检查驱动
  build/              构建脚本和版本资源
shared/sprites/       已确认的原始像素素材
 docs/                配置、检查摘要、限制、授权选项及演示
```

## 限制与检查范围

已有46项自动测试及实际 Windows EXE 启动、退出、配置恢复、重复启动、异常结束后重启和当前双屏检查记录。本次发布整理未新增测试项目或重新执行这些测试，见 [检查摘要](docs/TEST-REPORT.md)。

EXE 未签名，可能出现未知发布者或 SmartScreen 提示。新二进制未重新做两小时耐久、Defender 扫描或独立干净电脑验收；未穷尽物理热插拔、睡眠恢复、远程桌面及登录启动。坐下/起身为离散姿态切换，非整数缩放可能有不等宽像素台阶；见 [已知限制](docs/KNOWN-ISSUES.md) 和 [Windows安全说明](docs/SECURITY-AND-WINDOWS.md)。

不包含 AI 对话、语音、重力或复杂物理。活动检测读取输入时间戳和鼠标位置，不记录键盘内容。

## 授权与使用

程序源码、测试和构建/启动脚本采用 [MIT License](LICENSE-CODE-MIT.txt)，Copyright (c) 2026 WilliamZXT。

春喜的角色设计、像素图、动画帧、图标及其他美术素材不纳入 MIT，保留美术版权。用户可以下载、安装和使用官方桌宠程序；美术素材不得未经许可单独提取、转载、修改或用于其他商业产品。本项目未添加 CC BY-NC 或其他美术许可证。第三方组件按各自条款使用，声明保留在 THIRD-PARTY-NOTICES/。
