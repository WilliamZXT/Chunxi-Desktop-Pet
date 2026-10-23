# 已知限制 / Known limitations

- EXE未签名，SmartScreen可能提示；没有新Defender或真实公网下载信誉结果。
- 姿态切换为完整离散帧，没有坐下/起身中间素材；非整数缩放可能有不等宽像素阶梯。
- 未穷尽热插拔、休眠恢复、远程桌面和不同显卡；置顶可能被安全桌面或独占全屏覆盖。
- 登录启动登记逻辑已检查，但未实际注销登录验收。移动程序或配置后需重新保存启动设置。
- 新二进制未新增两小时耐久或独立干净机器验收。已有检查范围见 TEST-REPORT.md。
- 配置备份不自动清理。程序代码采用MIT，美术版权保留，具体限制见README。

Unsigned executable; discrete pose changes; fractional pixel steps; incomplete device/hotplug/resume/login coverage. No new endurance or clean-machine acceptance. Configuration backups require manual housekeeping. Code uses MIT; artwork copyright is reserved as described in the README.
