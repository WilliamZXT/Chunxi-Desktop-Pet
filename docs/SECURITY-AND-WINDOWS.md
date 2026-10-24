# Windows 安全说明 / Windows security notes

## 签名与历史检查 / Signing and historical checks

现有 v0.1.1 EXE 未签名。早期本地记录称，2026-10-22 在 Defender 实时保护启用时对一份 v0.1.1 分发目录执行了扫描，未发现匹配威胁记录；该记录没有足够的对应哈希证据证明它适用于后来最终上传的 Windows ZIP，因此不把它作为当前附件的扫描通过结论。本轮只整理文档，不运行新的防病毒或 SmartScreen 信誉测试。

The existing v0.1.1 EXE is unsigned. An earlier local record reports a Defender scan of a v0.1.1 distribution directory on 2026-10-22, with real-time protection enabled and no matching threat record. That record lacks sufficient hash linkage to establish coverage of the later uploaded Windows ZIP; it is not treated as a scan pass for the current asset. This pass edits documentation and runs no new antivirus or SmartScreen reputation test.

未关闭保护、添加排除项、改变 SmartScreen 策略，亦未把项目上传到第三方扫描网站。Defender 威胁扫描与 SmartScreen 下载信誉是不同检查；哈希一致也不等于安全保证。

Protection was not disabled, exclusions were not added, SmartScreen policies were not changed, and the project was not submitted to third-party scanning sites. Defender threat detection and SmartScreen download reputation are separate checks; a matching hash is not a safety guarantee.

## 遇到提示时 / If Windows warns

1. 从 [官方 v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) 取得原始 Windows ZIP，按 [校验指南](CHECKSUMS.md) 核对对应行。
2. 未签名软件可能提示未知发布者。根据自己的信任判断决定是否运行；企业策略拦截或威胁检测时停止，并保留版本、哈希和检测名称反馈。
3. 不建议关闭 Defender/SmartScreen 或排除整个下载目录，也不把所有检测一概称为误报。

1. Obtain the original Windows ZIP from the [official v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) and compare its entry using the [checksum guide](CHECKSUMS.md).
2. Unsigned software may show an unknown-publisher warning. Decide whether to run it based on your own trust assessment. Stop on an enterprise-policy block or threat detection and report the version, hash, and detection name.
3. Do not disable Defender/SmartScreen or exclude the entire download folder; detections are not automatically false positives.

Microsoft 对应用信誉的说明见 [SmartScreen 应用信誉](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)。代码签名及误报提交由维护者另行安排，本轮未购买证书或代为提交文件。敏感问题见 [安全报告政策](../SECURITY.md)。

See Microsoft's [SmartScreen app-reputation documentation](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation). Code signing and false-positive submissions require separate maintainer action; this pass purchases no certificate and submits no files. See the [security reporting policy](../SECURITY.md) for sensitive issues.
