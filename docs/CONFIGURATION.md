# 配置 / Configuration

默认EXE读取 `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`；源码默认读取 `desktop/build/config.json`。`--config PATH` 优先，设置保存写回实际加载的文件。默认模板只补缺失字段，不覆盖合法用户值。

个人配置及专用预设不随仓库和发行包提供；请用右键设置修改自己的大小和行为偏好，手动编辑后重启。

- scale 支持0.5–3.0，0.8合法；6.0修正到3.0。概率0–1，时间区间为两个正的有限数，睡眠最短时间晚于猫饼最长时间。
- poll_ms沿用20–2000整数毫秒；鼠标活动及拖拽阈值为正整数。
- 损坏JSON和错误字段会提示并安全恢复。修复或界面保存前先备份原文件；备份失败不覆盖，保存采用同目录临时文件替换。
- 合法配置加载不改写；旧未知字段保留。transition_ms是保留的旧字段，当前整帧绘制不使用它。
- 登录启动默认关闭；启用时保留显式配置路径。备份文件不会自动删除。

Personal configurations and presets are not distributed. Direct EXE launch preserves existing AppData preferences. Defaults fill missing fields only. UI saves use the active path. Invalid configuration is backed up before safe repair; backup failure prevents overwrite. Valid 0.8 remains unchanged. Restart after manual edits.
