# 更新记录 / Changelog

## 相对原始发行构建的后续修整 / Refinements relative to the original release build

这些改动保留在当前源码和文档中，没有替换 v0.1.1 的 Windows 附件，也没有创建新版本。
These changes are on current main without replacing the v0.1.1 Windows asset or creating a new version.

- 当前 main 包含后续 50%–300% 滑块、配置/帮助菜单、明确暂停状态和配置容错备份；不把这些算作原始下载包功能。
  Current main includes the later 50%–300% slider, config/help menus, clear pause status and configuration recovery/backups; these are not attributed to the original download.
- 打盹左耳下方轮廓按确认样式补圆，并同步六帧、静态预览与 GIF；其他姿态保留。
  Rounded the approved local contour below the left ear across six napping frames and matching previews; other poses remain unchanged.
- 演示留白和锚点整理；公开姿态统一为“卧着观察 / Resting and watching”和“打盹 / Napping”，保留兼容性文件名与配置键。
  Refined preview padding/anchors and standardized pose names while retaining compatible filenames and configuration identifiers.
- 补齐中英文主页、使用与配置、安全、校验、已知问题、发布与验证范围说明。
  Completed bilingual homepages and guides covering use, configuration, security, checksums, limitations, release notes and validation scope.

## v0.1.1 — 已正式发布 / Published

实际发布信息以 [GitHub v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) 为准。
The [GitHub v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) is the publication record.

- 独立 Windows 便携桌宠：透明、无边框、可置顶和拖拽。
  Standalone portable Windows pet with a transparent borderless window, optional topmost behavior and dragging.
- 坐姿呼吸、随机眨眼/耳抖、空闲卧着观察/打盹及输入活动唤醒，观察与点击反应带概率和冷却。
  Breathing, randomized blinks/ear twitches, idle resting/napping, activity-based wake-up, and probabilistic observation/click reactions with cooldowns.
- 设置内 50%–200% 大小数值框、暂停勾选、位置记忆及可选登录启动。
  A 50%–200% numeric size field in Settings, pause checkbox, position memory and optional login startup.
- 有基础配置范围校验，0.8 大小合法；后续安全恢复/备份和便捷菜单不在原始附件内。
  Basic configuration-range checks accept 0.8 scale; later safe recovery/backups and convenience menus are absent from the original asset.

历史版本不删除；版本号 0.1.0 若出现在用户旧配置中，不等同于当前程序版本。
Historical versions are retained. A 0.1.0 schema label in an older personal configuration is not the current application version.

标签来源补充：`v0.1.1` 标签指向 `453b74cf836b8de45056b32fbd7f3403bcba542f`，其应用源码与当前 main 相同，含原始 Windows 附件没有的后续功能，因此 GitHub 自动标签源码包不能视为该 EXE 的精确构建输入。本地历史源码归档（SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`）的 11 个应用模块、启动入口与内嵌代码静态一致，9 项随包资源字节一致；该归档尚未公开附加，精确历史 Git 提交与可重复二进制构建未建立。

Tag provenance: `v0.1.1` points to `453b74cf836b8de45056b32fbd7f3403bcba542f`. Its application source matches current main and includes later features absent from the original Windows attachment; GitHub's tag-source archive is therefore not the exact input for that EXE. A local historical source archive (SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`) statically matches all 11 application modules and the entry point, with nine identical bundled resources. It is not publicly attached; its exact historical Git commit and a reproducible binary build are not established.
