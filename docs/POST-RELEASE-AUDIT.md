# 发布后文档整理报告 / Post-release documentation audit

## 范围 / Scope

基于当前公开 main `662ec4764bbbdbb8698f62d36897dcef6b51ab53` 的完整快照，以及实际已发布的 v0.1.1 Release 信息和下载附件。只修改文档、许可证适用范围说明和构建工具生成的使用说明文字；不改变程序逻辑、JSON 默认值、像素/动画、个人配置、现有版本或 Release 附件。

Based on a complete snapshot of public main at the commit above, plus live published v0.1.1 metadata and downloaded assets. Changes cover documentation, license-scope explanation and generated usage text only. Application logic, JSON defaults, artwork/animation, personal settings, versions and Release assets are unchanged.

## 文件清单 / File inventory

| 文件 / File | 整理内容 / Change |
|---|---|
| README.md / README.en.md | 同结构中英文主页、明显下载与语言切换、演示、设置、校验、反馈、版本边界 / Matching full homepages, download/language links, demos, settings, checksums, feedback and artifact scope |
| CHANGELOG.md | 发布后 main 与固定发行包分开，去掉发布准备状态 / Separate post-release main from fixed release assets; remove preparation status |
| LICENSE-CODE-MIT.txt | 增加中文适用范围，标准英文 MIT 正文保留 / Chinese scope added; standard English MIT legal text retained |
| docs/CONFIGURATION.md | 完整双语参数、实际默认值与校验规则、配置路径 / Complete bilingual parameter/default/validation and path guidance |
| docs/KNOWN-ISSUES.md | 完整双语限制，不将已修复项列为未实现 / Full bilingual limitations; implemented fixes distinguished |
| docs/LICENSE-OPTIONS.md | MIT 代码与保留美术权利、重新打包限制 / MIT code versus reserved artwork rights and repackaging limits |
| docs/SECURITY-AND-WINDOWS.md | 双语未签名与安全指引，限定历史 Defender 记录 / Bilingual unsigned/security guidance and scoped historical scan evidence |
| docs/TEST-REPORT.md | 历史、源码、本地 EXE、当前文档检查明确区分 / Separate historical, source, local EXE and current documentation evidence |
| lite/README.md | 补齐宿主快照范围与英文说明 / Complete bilingual host-snapshot scope |
| desktop/README.md（新增 / new） | Windows 使用、源码运行、构建与依赖 / Windows use, source setup, builds and dependencies |
| docs/README.md（新增 / new） | 双语文档导航与内部文件例外 / Bilingual documentation index and developer-file exemptions |
| docs/USER-GUIDE.md（新增 / new） | 中英菜单、常见启动提示、位置、配置与反馈 / Menu/launcher translations, position, settings and feedback |
| docs/CHECKSUMS.md（新增 / new） | 正式附件校验值及历史额外清单范围 / Published asset hash and historical extra checksum entries |
| docs/RELEASE-NOTES.md（新增 / new） | 可直接用于 v0.1.1 正文的完整双语说明 / Complete bilingual body suitable for v0.1.1 |
| docs/media/README.md（新增 / new） | 每个 GIF/静态图双语说明，标明历史预览 / Bilingual captions and historical-still labels |
| SECURITY.md（新增 / new） | 普通与敏感问题报告说明 / Ordinary versus sensitive issue reporting |
| docs/POST-RELEASE-AUDIT.md（新增 / new） | 本报告 / This report |
| desktop/build/finalize_distribution.py | 仅改生成的使用说明文本：补英文和授权、去旧姿态名；不运行构建 / Generated usage text only: English, licensing and pose names; no build run |

## 术语与例外 / Terminology and exemptions

公开文档统一：春喜 / Chunxi；春喜桌宠 / Chunxi Desktop Pet；卧着观察 / Resting and watching；打盹 / Napping；自动行为 / Automatic behaviors；行为配置 / Behavior configuration。兼容性文件名 `loaf-source.gif`、`dozing-source.gif`、JSON 键和内部状态标识保持，不通过改键名破坏程序。

User-facing terms follow the bilingual equivalents above. Legacy filenames, JSON keys and internal state identifiers remain compatible rather than being renamed for prose consistency.

依赖锁定、VERSION、Windows 版本元数据、机器 JSON、开发测试脚本和实现注释不强制双语。标准 MIT 法律正文保留英文。现有程序 UI/日志主要为原有语言，本轮没有改程序；使用指南提供中英对照，不声称已有英文界面。

Dependency pins, VERSION, Windows metadata, machine JSON, tests and implementation comments are not forced into bilingual form. Standard MIT legal text remains English. Application UI/log strings retain their existing language; the guide supplies translations without claiming an English UI.

## 实际检查及限制 / Checks and limits

- 对全部当前仓库文件做快照与 Git blob 哈希核对；扫描文本中的私人路径与常见凭据模式。模式扫描未发现并不等于完整秘密审计，也不覆盖所有历史提交。
  Snapshot and Git-blob hash comparison cover the current tree; text is scanned for personal paths and common credential patterns. A clean pattern scan is not a comprehensive secret audit or a scan of every historical commit.
- 实际下载 Windows ZIP，SHA-256 为 `8f1cc6d990ff135374f92036097f86023639ddad5662e08c3ec862a3e6869c01`，与当前发布校验文件及 GitHub asset digest 一致；ZIP CRC 检查通过。没有运行或替换这个下载包。
  The Windows ZIP was downloaded and its SHA-256 matches the published list and GitHub asset digest; ZIP CRC verification passed. The downloaded package was not run or replaced.
- 已发布 ZIP 内含历史中文文档、旧姿态名和发布准备说明；保留附件的前提下不能在本轮改写包内文本。以当前双语网页文档为准，不把这些历史包内文档说成已翻译。
  The published ZIP contains historical Chinese documents, older pose names and preparation wording. Those embedded texts cannot be rewritten while preserving the attachment. Current bilingual web documentation is the updated reference; embedded historical documents are not claimed as translated.
- `SHA256SUMS.txt` 列出未单独上传的源码包及文档；仅 Windows ZIP 对应行用于当前可运行下载。清单未替换；GitHub 自动源码包不套用历史源码包哈希。
  The checksum file names unattached historical source/docs. Use its Windows ZIP entry for the runnable download. The file is unchanged; automatic GitHub source archives do not use the prepared-source hash.
- 实际公开 EXE 与后续 main 不同：静态内嵌代码检查确认设置界面 50%–200%，没有后续大小滑块、配置/帮助入口及安全恢复备份；默认 JSON 虽相同，能力不完全相同。未运行这个 EXE。
  Static embedded-code inspection confirms an earlier public EXE with 50%–200% Settings and no later slider, config/help menus or safe recovery/backups. JSON defaults match, but capabilities differ. The EXE was not run.
- 本轮只执行文档/链接/完整性检查；没有重新运行应用、自动运行测试、长时间耐久、Defender、SmartScreen 信誉或硬件验收。
  This pass performs documentation/link/integrity checks only, not application execution, runtime tests, endurance, antivirus, reputation or hardware acceptance.

## 仍需维护者网页操作 / Maintainer web actions still required

当前文件连接器没有编辑 Release 正文、About 和 Topics 的接口，未找到 GitHub CLI；本轮没有绕过先前浏览器访问限制或提取令牌。
The current file connector exposes no Release-body, About or Topics editor, and no GitHub CLI was found. This pass does not bypass prior browser restrictions or extract tokens.

1. 在 [v0.1.1 Release](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) 点击 Edit，用 [发布说明](RELEASE-NOTES.md) 替换正文；保留标签、标题、两个附件，不创建新版本。
   Edit that existing Release and replace its body with [release notes](RELEASE-NOTES.md). Keep the tag, title and two assets; do not create a new version.
2. About 描述建议：`安静陪伴你的 Windows 像素奶牛猫桌宠。A quiet pixel-art tuxedo cat companion for Windows.`；Website 指向 v0.1.1 Release。
   Suggested bilingual About description is above; point Website to the existing v0.1.1 Release.
3. 建议 Topics：`desktop-pet`、`pixel-art`、`tuxedo-cat`、`windows`、`pyside6`、`python`、`desktop-companion`。
   Suggested Topics are the relevant tags above.

这些网页字段仍是待办，不因为仓库文档已提交而自动完成。完整逐链接结果保存在本次本地交接报告中，不能把路径检查等同于浏览器连续播放验收。
These web fields remain pending after the file commit. Full per-link results are retained in the local handoff; path checks are not continuous browser-playback acceptance.
