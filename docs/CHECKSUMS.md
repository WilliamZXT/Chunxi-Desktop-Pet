# SHA-256 校验 / SHA-256 verification

## 核对 Windows 包 / Check the Windows package

从同一 [v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) 取得 [Windows ZIP](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip) 和 [SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)，完整下载后在下载目录执行：

Download the [Windows ZIP](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip) and [SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt) from the same [v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1). After both downloads finish, run in that directory:

```powershell
Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256
```

发布时该文件的 SHA-256 为 / Published Windows ZIP SHA-256:

```text
8f1cc6d990ff135374f92036097f86023639ddad5662e08c3ec862a3e6869c01
```

比较校验文件中 **ChunxiDesktopPet-v0.1.1-win-x64.zip** 对应行；大小写不影响哈希含义。若不一致，停止使用该副本，重新检查来源和下载完整性并反馈。校验只能证明与所比较的文件一致，不等于代码签名、安全保证或 SmartScreen 信誉通过。

Compare the line for **ChunxiDesktopPet-v0.1.1-win-x64.zip**; hexadecimal letter case does not matter. On mismatch, stop using that copy, check the source/download, and report it. A matching hash is an integrity check, not a code signature, security guarantee, or SmartScreen reputation approval.

## 当前校验清单的范围 / Scope of the current checksum list

当前 Release 只有 Windows ZIP 与 `SHA256SUMS.txt` 两个手动上传附件。清单还列出历史准备阶段的源码包和独立文档；这些文件未单独附加到当前 Release。不要把清单当作实际附件清单，也不要用这些历史值核对当前 main 的 README 或文档。

The current Release has two manually uploaded assets: the Windows ZIP and `SHA256SUMS.txt`. Its checksum list also names a historical prepared source archive and standalone documents that are not separately attached. It is not an asset inventory, and those historical hashes do not verify the evolving README or documents on main.

GitHub 自动生成的 Source code (zip/tar.gz) 与历史 `chunxi-pet-v0.1.1-source.zip` 不是同一个文件，不应套用该行哈希。当前源码来自仓库，历史标签内容来自 v0.1.1 标签；都不是可直接运行的 Windows 包。本次保留原始校验附件，不重新生成或上传。

GitHub's automatic Source code (zip/tar.gz) archives are not the historical `chunxi-pet-v0.1.1-source.zip`; do not apply that row's hash to them. Current source comes from the repository; historical source comes from the v0.1.1 tag. Neither is the ready-to-run Windows package. This documentation pass preserves the published checksum asset without replacing it.
