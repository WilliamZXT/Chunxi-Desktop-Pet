# 检查摘要与证据范围 / Validation summary and evidence scope

## 中文

请区分源码检查、本机 EXE 检查、历史二进制记录和公开发行包。相同版本号不证明文件字节相同。

| 范围 | 实际记录 | 不代表什么 |
|---|---|---|
| 原发布整理记录 | 记录了 46 项自动测试，以及 Windows EXE 启停、重复启动、异常结束后重启、配置损坏/scale 越界恢复和缺失资源检查 | 本轮没有重跑，也不是所有 Windows 机器通过 |
| 早期窗口检查 | 透明、置顶、拖拽和当前 100%/150% 双屏有本地记录 | 未覆盖全部硬件、物理热插拔、远程桌面、睡眠恢复 |
| 后续打盹轮廓修补 | 46 项源码自动测试通过；本机可运行目录 EXE --check 可加载 24 个动作；只改变 sleep，其余 23 个 clip 保持；GIF 解码播放两轮、静态图与第一帧一致 | 可运行目录仅替换外部美术，原始 Release 附件未替换；不把离屏解码当作浏览器目视验收 |
| 本轮公开文档整理 | 当前仓库快照、参数/版本静态核对、文档双语覆盖、链接/图片路径及 Release 附件清单检查 | 不新增程序功能、不重建 EXE、不重跑长时间运行或硬件测试 |

短状态检查中缩短等待或注入活动的记录，不算自然耐久测试。沙盒 EXE 检查可能重定向用户目录，不作为正常桌面用户配置路径的验收。历史二进制 `5207003eee6c939bc7641648ee08cd071a9b67b7f696a99049c1f98c136e879e` 是某次本地 EXE 的哈希，不是公开 Windows ZIP 的校验值。

本轮对公开附件做了只读内嵌代码检查（未执行 EXE）：实际 EXE 哈希为 `078c10350ad8c356bd3a7b34b16fa2421fe1806c9c8ce406e1756aaa6a32d1b8`，其设置大小为 50%–200%，没有当前 main 的后续便捷菜单与安全恢复备份。默认 JSON 与 main 一致，但不能据此认定程序能力一致。

当前下载包应按 [SHA-256 指南](CHECKSUMS.md) 核对。没有对当前附件宣称新的两小时耐久、Defender、真实公网 SmartScreen、独立干净机器或实际登录启动验收。详细未验证项见 [已知问题](KNOWN-ISSUES.md)。

## English

Distinguish source checks, local EXE checks, historical binary records, and the published package. An identical version number does not establish identical bytes.

| Scope | Recorded evidence | What it does not establish |
|---|---|---|
| Original publication preparation | 46 automated tests and recorded Windows lifecycle, duplicate-instance, abnormal-exit recovery, malformed/scale-out-of-range configuration, and missing-resource checks | No rerun in this pass; no pass claim for all Windows machines |
| Earlier window checks | Local transparency, topmost, drag and current 100%/150% dual-display records | Not all hardware, physical hotplug, Remote Desktop or sleep/resume |
| Later napping-contour repair | 46 source tests passed; local runnable EXE --check loaded 24 clips; only sleep changed, with 23 other clips preserved; two GIF decoder loops and a still-frame match | Only external artwork changed in that local folder; Release assets stayed unchanged; offscreen decoding is not browser visual acceptance |
| This public-documentation pass | Current repository snapshot, static parameter/version comparison, bilingual coverage, document/image paths, links and Release asset inventory | No new app feature, EXE rebuild, endurance rerun or hardware test |

Accelerated state checks and injected activity are not natural-duration endurance tests. Sandboxed EXE checks can redirect user folders and do not establish the ordinary desktop user's active configuration path. Historical hash `5207003eee6c939bc7641648ee08cd071a9b67b7f696a99049c1f98c136e879e` identifies a local EXE, not the public Windows ZIP.

This pass inspected embedded code in the public EXE without executing it. EXE hash: `078c10350ad8c356bd3a7b34b16fa2421fe1806c9c8ce406e1756aaa6a32d1b8`. Its size UI is 50%–200%, without current-main convenience menus or safe recovery/backups. Matching JSON defaults do not prove matching capabilities.

Use the [SHA-256 guide](CHECKSUMS.md) for the published download. No new two-hour endurance, Defender, real public-download SmartScreen, independent clean-machine or actual login-startup acceptance is claimed for that asset. See [known issues](KNOWN-ISSUES.md) for remaining coverage gaps.

## 最终来源核对 / Final provenance check

标签来源补充：`v0.1.1` 标签指向 `453b74cf836b8de45056b32fbd7f3403bcba542f`，其应用源码与当前 main 相同，含原始 Windows 附件没有的后续功能，因此 GitHub 自动标签源码包不能视为该 EXE 的精确构建输入。本地历史源码归档（SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`）的 11 个应用模块、启动入口与内嵌代码静态一致，9 项随包资源字节一致；该归档尚未公开附加，精确历史 Git 提交与可重复二进制构建未建立。

Tag provenance: `v0.1.1` points to `453b74cf836b8de45056b32fbd7f3403bcba542f`. Its application source matches current main and includes later features absent from the original Windows attachment; GitHub's tag-source archive is therefore not the exact input for that EXE. A local historical source archive (SHA-256 `a18e783ff250f536d4f70116afba1b92e5d4d25abc42db41bed395de0d69fd00`) statically matches all 11 application modules and the entry point, with nine identical bundled resources. It is not publicly attached; its exact historical Git commit and a reproducible binary build are not established.

另查阅到绑定已发布 EXE 哈希的历史运行记录：7200.281 秒完成，未加速或注入状态，记录无错误；不是本轮重跑，也不能用于当前 main 的后续构建。
A historical run record tied to the published EXE hash completed after 7200.281 seconds, without acceleration/state injection or recorded errors. This was not rerun in this pass and does not validate later current-main builds.
