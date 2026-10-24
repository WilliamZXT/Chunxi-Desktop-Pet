# 行为配置 / Behavior configuration

[文档索引 / Documentation](README.md) · [使用指南 / User guide](USER-GUIDE.md)

## 适用构建 / Build scope

本参数表及下方自动恢复规则针对当前 main。已发布 v0.1.1 Windows 包的默认 JSON 值相同、基础 scale 校验支持 0.5–3.0（0.8 合法），但其设置界面只提供 50%–200%，没有后续的安全恢复、自动备份或“打开当前配置文件”菜单。非法 JSON 或越界值可能阻止原发行包启动，编辑前请手动备份。不要把 current main 的修复能力当作已上传附件的能力。

The parameter table and recovery rules describe current main. The published v0.1.1 Windows package has matching JSON defaults and basic scale validation for 0.5–3.0 (including 0.8), but its Settings UI exposes only 50%–200%. It lacks later safe recovery, automatic backups and the open-active-config menu. Invalid JSON or out-of-range values can prevent that original build from starting: back up manually before editing. Current-main fixes are not automatically present in the uploaded attachment.

## 配置位置与优先级 / Location and precedence

EXE 默认读取 `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`；源码默认读取 `desktop/build/config.json`。`--config PATH` 优先。Windows 应用容器等环境可能重定向用户目录，应以菜单“打开当前配置文件”显示的实际文件为准。界面保存写回该文件。默认模板补缺失字段，不覆盖合法用户值；本仓库不分发个人配置。

The EXE normally reads `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`; source runs use `desktop/build/config.json`. `--config PATH` takes precedence. Windows app containers can redirect user folders; **打开当前配置文件** opens the file actually in use. UI saves target that file. Defaults fill missing fields without replacing valid user values. Personal configurations are not distributed.

下面的值来自 [default.json](../desktop/config/default.json)，范围来自当前验证代码；时间单位为秒，另有标注除外。`loaf` 和 `sleep` 是兼容性配置键，界面文档称“卧着观察”和“打盹”，无需改键名。

Values below come from [default.json](../desktop/config/default.json); supported ranges follow the current validator. Times are in seconds unless stated otherwise. Legacy identifiers `loaf` and `sleep` remain unchanged for compatibility; their user-facing names are Resting and watching and Napping.

| 参数 / Key | 默认 / Default | 说明与规则 / Meaning and rule |
|---|---|---|
| `version` | `0.1.1` | 配置格式版本，加载时归一化 / Configuration schema version, normalized on load |
| `window.scale` | `1.0` | 大小 50%–300%；`0.8` 合法；`6.0` 限制到 `3.0` / Size 50%–300%; 0.8 is valid; 6.0 is clamped to 3.0 |
| `window.always_on_top` | `true` | 布尔值，始终置顶 / Boolean, always on top |
| `window.position` | `null` | 空值或两个有符号 32 位整数；已保存运行位置优先 / Null or two signed 32-bit integers; saved runtime position takes precedence |
| `preferences.frequency` | `normal` | `quiet` / `normal` / `more`，见下方 / See frequency rules below |
| `behavior.loaf_after_seconds` | `[50, 95]` | 卧着观察的总空闲阈值 / Total idle threshold for resting and watching |
| `behavior.sleep_after_seconds` | `[210, 330]` | 打盹总空闲阈值；最小值须大于上项最大值 / Total idle threshold for napping; minimum must exceed the resting maximum |
| `behavior.blink_interval_seconds` | `[12, 28]` | 眨眼随机间隔 / Random blink interval |
| `behavior.ear_interval_seconds` | `[65, 145]` | 耳抖随机间隔 / Random ear-twitch interval |
| `behavior.look_cooldown_seconds` | `[45, 100]` | 鼠标观察冷却 / Pointer-observation cooldown |
| `behavior.click_cooldown_seconds` | `[30, 70]` | 点击机会冷却，不回应也消耗机会 / Click-opportunity cooldown, including non-responses |
| `behavior.look_probability` | `0.22` | 0–1，进入附近区域时的候选概率 / 0–1 candidate chance when entering the nearby area |
| `behavior.click_probability` | `0.4` | 0–1，符合条件时的候选概率 / 0–1 candidate chance when eligible |
| `behavior.near_radius_pixels` | `260` | 正的有限数，附近区域半径 / Positive finite proximity radius |
| `behavior.wake_seconds` | `1.5` | 正的有限数，唤醒过渡时间 / Positive finite wake-up duration |
| `interaction.poll_ms` | `100` | 20–2000 整数毫秒 / Integer milliseconds, 20–2000 |
| `interaction.mouse_move_threshold_pixels` | `3` | 正整数，活动检测阈值 / Positive integer, mouse-activity threshold |
| `interaction.drag_threshold_pixels` | `6` | 正整数，拖拽判定阈值 / Positive integer, drag threshold |
| `window.transition_ms`（旧字段 / legacy） | 无 / absent | 旧文件可保留，当前整帧绘制不使用 / May remain in older files; current full-frame rendering does not use it |

## 时间、频率与反应 / Timing, frequency and reactions

时间区间须是两个正的有限数；上下限反向会排序。当前代码没有统一的时间最大值，不应把建议间隔写成强制范围。概率限制到 0–1。鼠标半径和唤醒时间只要求正的有限数。

Time ranges must contain two positive finite numbers; reversed endpoints are sorted. There is no universal maximum interval in current code. Probabilities are clamped to 0–1. Radius and wake duration require positive finite values.

`quiet` 将眨眼、耳抖、观察和点击冷却的抽样时间乘 1.5，`normal` 为 1.0，`more` 为 0.8；不改变卧着观察/打盹空闲阈值，也不改变概率。动作会受状态、当前动作与冷却约束，不是到点必播。点击候选动作是轻抬爪或眨眼；部分重复反应被跳过。鼠标观察在进入附近范围时判断，不是停在旁边便连续触发。

`quiet` multiplies sampled blink/ear intervals and observation/click cooldowns by 1.5; `normal` uses 1.0 and `more` 0.8. These settings do not change idle thresholds or probabilities. State, ongoing actions, and cooldowns can defer or suppress a reaction. Click candidates are a small paw lift or blink; repeated reactions may be skipped. Pointer observation is evaluated on entering the nearby area, not continuously while remaining there.

## 编辑、恢复和位置 / Editing, recovery and position

优先使用设置界面。手动编辑时退出春喜、备份 JSON、保留英文键名和正确类型，保存后重启。错误类型恢复该参数默认值，越界大小与概率安全限制；损坏 JSON 会提示并恢复。修复或界面保存前先备份，备份失败不主动覆盖原文件；保存通过同目录临时文件替换。有效配置正常加载不改写，未知旧字段保留。备份不会自动删除。

Prefer the settings UI. For manual edits, exit Chunxi, back up the JSON, preserve keys and types, then restart. Invalid types fall back per field; out-of-range scale and probabilities are clamped. Malformed JSON produces a recovery notice. Repair/UI save backs up the original first; a failed backup prevents intentional overwrite. Saves use a temporary file in the same directory. Valid files are not rewritten on normal load; unknown legacy fields remain. Backups require manual cleanup.

正常退出时，位置另存于运行目录的 `runtime-state.json`，恢复时优先于 `window.position`。配置、运行位置、日志和备份不要提交到公开仓库。登录启动通过界面单独管理，默认关闭，不是此 JSON 中的开关。

On normal exit, position is stored separately in `runtime-state.json` under the runtime directory and takes precedence over `window.position`. Keep personal settings, state, logs and backups out of public commits. Login startup is managed separately through the UI and is off by default, not a switch in this JSON.
