# Windows Defender、SmartScreen与签名

## 本次实际记录

- EXE Authenticode状态为 `NotSigned`，没有用自签名冒充可信发布者。
- 2026-10-22在Defender实时防护启用的本机，对v0.1.1分发目录做本地自定义扫描，命令完成，未发现与该目录匹配的威胁检测记录。
- 没有关闭防护、添加排除项、改SmartScreen策略或上传素材到第三方扫描网站。
- 没有把本地文件伪装为已从GitHub下载来宣称SmartScreen通过；真实公网下载信誉测试尚未进行。

## 可能出现的提示

未签名的新应用可能出现“未知发布者”或“Windows已保护你的电脑”等提示。SmartScreen会评估文件和发布者信誉；即使签名，新文件也可能在信誉建立前被提示。见 [Microsoft应用信誉说明](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)。

Defender恶意软件检测与SmartScreen下载信誉不是同一次检查，本机未检出不代表所有电脑和安全产品都会放行。

## 建议处理

1. 从维护者的同版Release取得文件，不使用来源不明的重打包版本。
2. 核对同版 `SHA256SUMS.txt`；可运行 `Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256`。
3. 若有病毒检测或企业策略拦截，停止运行，保留版本、哈希、检测名称和截图，联系发布者核实。
4. 不关闭Defender/SmartScreen，不为整个下载目录设置排除项，不把所有提示一概称为误报。

可信代码签名、Microsoft误报处理及对外授权由发布者安排。本次没有购买/借用证书，也没有替用户提交文件。
