# 检查摘要 / Validation scope

本次只整理首次发布材料，不增加测试或功能，不重新执行旧测试。

已核对上轮记录：46项自动测试通过；实际Windows EXE的启动、退出、重新启动、重复实例、强制结束后恢复、scale6.0与非法JSON恢复、缺失资源检查通过。Qt窗口还检查透明、置顶、拖拽及当前100%/150%双屏。短状态检查用了缩短等待和注入活动信号，不能算自然耐久测试。

沿用二进制SHA-256：5207003eee6c939bc7641648ee08cd071a9b67b7f696a99049c1f98c136e879e。

本轮仅做文件清单、敏感信息模式扫描、共享资源哈希、ZIP完整性及下载SHA-256核对。不把这些归为新运行测试。

新构建未重新做两小时耐久、Defender、真实公网SmartScreen、独立干净机器、物理热插拔、实际登录启动等验收。决定发布不等于这些项目已经通过。

Existing automated/runtime evidence is retained; this publication pass adds no new tests. New endurance, Defender, real download reputation and clean-machine acceptance are not claimed. Packaging and privacy checks are static/integrity checks only.
