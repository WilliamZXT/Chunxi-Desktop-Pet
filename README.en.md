# Chunxi Desktop Pet

**[中文](README.md) · [Download v0.1.1](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1) · [User guide](docs/USER-GUIDE.md) · [Documentation](docs/README.md)**

Meet Chunxi (春喜), a round-faced pixel-art tuxedo cat with amber eyes and a quiet, slightly aloof personality. Chunxi Desktop Pet keeps you company with gentle breathing, occasional watching, and naps. This standalone Windows application uses Python and PySide6; normal operation requires neither ChatGPT/Codex nor an internet connection.

## Animation previews

### Sitting · blinking · ear movement

![Chunxi sitting, blinking and moving its ears](docs/media/idle-source.gif)

### Resting and watching

![Chunxi resting and watching](docs/media/loaf-source.gif)

### Napping

![Chunxi napping](docs/media/dozing-source.gif)

[Napping still frame](docs/media/dozing-preview.png) · [All preview images and captions](docs/media/README.md)

These GIFs preview existing animation assets, not real-time automatic behaviors. Playback speed does not represent action frequency. They reflect current `main`, including a post-release local repair to the napping contour. **The published v0.1.1 Windows attachment has not been replaced**, so its artwork details may differ from current source previews.

## Download and start

**Current published version: [v0.1.1](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/tag/v0.1.1).** For Windows x64, download **[ChunxiDesktopPet-v0.1.1-win-x64.zip](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/ChunxiDesktopPet-v0.1.1-win-x64.zip)** and **[SHA256SUMS.txt](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/releases/download/v0.1.1/SHA256SUMS.txt)**.

1. Extract the entire ZIP, exit any older instance, then double-click `ChunxiDesktopPet.exe`.
2. Keep the full folder, especially `_internal/`. Do not move the EXE alone or run it from inside the archive.
3. The Windows package includes runtime dependencies; no separate Python installation or administrator access is required.
4. GitHub's automatic **Source code (zip/tar.gz)** downloads contain source code, not a ready-to-run Windows application.

Open PowerShell in your download folder and check the Windows ZIP entry:

```powershell
Get-FileHash .\ChunxiDesktopPet-v0.1.1-win-x64.zip -Algorithm SHA256
```

Compare the result with the matching filename in the release's checksum file. That file also lists historical filenames not attached separately to this Release; it does not verify a README that has since changed. See the [SHA-256 guide](docs/CHECKSUMS.md). Embedded package documents are historical Chinese texts with some outdated instructions; current bilingual web guides describe actual build differences.

The EXE is unsigned and SmartScreen may show an unknown-publisher warning. Check the source and hash. Stop and report any threat detection or policy block rather than disabling protection. See [Windows security notes](docs/SECURITY-AND-WINDOWS.md).

## Current source versus the published package

The actual downloaded EXE has SHA-256 `078c10350ad8c356bd3a7b34b16fa2421fe1806c9c8ce406e1756aaa6a32d1b8`; it is an earlier build, not the later local polish build. **Matching defaults do not establish identical features.**

| Area | Published v0.1.1 Windows package | Current main |
|---|---|---|
| Size UI | Numeric field in Settings, 50%–200% | Adjust size slider and settings, 50%–300% |
| Configuration access | No dedicated open-config/help menu | Open configuration and parameter-help menus |
| Pause/resume | Check 暂停自动行为 to pause; uncheck to resume | Explicit pause/resume status wording |
| Configuration recovery | Basic range validation; malformed JSON/out-of-range values can prevent startup; no later recovery/backup implementation | Per-field validation, safe correction, notices and backup before repair |
| Napping artwork | Original release assets | Approved left-contour repair |

Advanced menu and recovery descriptions below refer to current source. Download users should manually back up JSON before editing; the original package must not be assumed to repair invalid settings automatically. This pass does not replace assets. See the [user guide](docs/USER-GUIDE.md).

## Features and controls

- Transparent, borderless window with optional always-on-top behavior, drag-to-move, position memory on normal exit, and visibility adjustment when screen layouts change.
- Gentle breathing, randomized blinks and ear twitches; resting and watching, then napping after inactivity; a gradual wake-up after input activity.
- Occasional watching when the pointer enters the nearby area. Clicks may trigger a blink or small paw lift, with cooldowns. Dragging does not also trigger a click.
- Right-click Chunxi or its tray icon. The current UI uses Chinese labels; translations are provided below and in the [user guide](docs/USER-GUIDE.md).

The table describes current source. The original package offers Settings, the pause checkbox, position reset, logs and exit.

| Actual menu label | English meaning and action |
|---|---|
| 调节大小… | Adjust size: live 50%–300% preview; Save keeps it, Cancel restores it |
| 设置… | Settings: size, always on top, behavior frequency, optional login startup |
| 暂停自动行为 / 恢复自动行为（当前已暂停） | Pause automatic behaviors / Resume automatic behaviors; the current animation can continue |
| 回到屏幕右下方 | Return to the lower-right corner |
| 打开当前配置文件 / 配置参数说明 | Open the active configuration / Configuration help |
| 打开日志文件夹 | Open logs; remove personal paths before sharing |
| 退出春喜 | Exit Chunxi |

Login startup is off by default and activates only when selected and saved. Save that setting again after moving the program. AI conversation, voice, gravity, and window-edge perching are not included.

## Automatic behaviors and behavior configuration

These are [factory defaults](desktop/config/default.json), not your personal settings. At `normal` frequency:

| Behavior | Default trigger |
|---|---|
| Blinking / ear twitch | Random 12–28 / 65–145 second intervals, subject to current state and other actions |
| Resting and watching / Napping | Random total-idle thresholds of 50–95 / 210–330 seconds |
| Wake-up | About 1.5 seconds after input activity is detected |
| Pointer observation | A 22% candidate chance on entering the nearby area; 45–100 second cooldown |
| Click reaction | A 40% candidate chance; 30–70 second cooldown; some repeated reactions are skipped |

Default `scale` is `1.0`; supported values are `0.5–3.0`, including `0.8` for 80% size. Frequency settings are Quiet, Normal, and A little more. A candidate chance does not guarantee a response to every input.

The EXE normally uses `%LOCALAPPDATA%/ChunxiDesktopPet/config.json`; source runs use `desktop/build/config.json`. `--config PATH` selects an explicit file. Environments may redirect user folders: use **打开当前配置文件** to find the actual active file. Valid user values take precedence; an upgrade should not overwrite personal settings with defaults. Restart after manual edits; UI changes apply when saved. Backups are not deleted automatically.

See [behavior configuration](docs/CONFIGURATION.md) for size, intervals, probabilities, proximity radius, mouse/drag thresholds, and recovery rules. Position is stored separately in `runtime-state.json` under the runtime directory on normal exit.

## Run and build from source

Use Windows x64 and Python 3.12. From `desktop/`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\run.py
```

Alternatively, run `setup.ps1`, then double-click `Start-Chunxi.cmd`. Recreate the virtual environment after moving source. PySide6 is pinned to 6.10.0. Builds use PyInstaller 6.16.0 and hooks 2026.9:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\build\build.ps1
```

Output: `desktop/build/dist/v0.1.1/ChunxiDesktopPet/`. Distribute the entire folder. See [development and running](desktop/README.md).

## Layout and documentation

`desktop/` contains the standalone app; `shared/sprites/` holds pixel assets; `lite/` preserves the host-pet snapshot and is not required by the desktop application. Documentation: [Use](docs/USER-GUIDE.md), [Configuration](docs/CONFIGURATION.md), [Known issues](docs/KNOWN-ISSUES.md), [Security](docs/SECURITY-AND-WINDOWS.md), [Validation scope](docs/TEST-REPORT.md), [Release notes](docs/RELEASE-NOTES.md), [Changelog](CHANGELOG.md).

## Limitations and feedback

Pose changes use discrete frames; fractional scaling can create uneven pixel steps. Physical hotplug, sleep/resume, Remote Desktop, and actual login startup have not been exhaustively validated. This documentation pass does not rerun runtime or endurance tests. Historical evidence and current link/document checks are distinguished in the [validation summary](docs/TEST-REPORT.md).

Report problems through [GitHub Issues](https://github.com/WilliamZXT/Chunxi-Desktop-Pet/issues), including the app and Windows versions, display scale, reproduction steps, and sanitized screenshots/logs. State whether you used a Release package or current source. For sensitive security reports, read [SECURITY.md](SECURITY.md). Future work follows known issues and the changelog; no new version date is promised.

## Licensing

Application source code, tests, and build/startup scripts use the [MIT License](LICENSE-CODE-MIT.txt). Chunxi character designs, pixel artwork, animations, icons, sprite sheets, and other artwork are excluded from MIT; artwork copyright is reserved. Users may download, install, and use the official desktop-pet application. Without permission, artwork must not be separately extracted, reposted, modified, repackaged, or used in commercial products. No CC or other artwork license is added.

Third-party components retain their own licenses. Notices are included under `THIRD-PARTY-NOTICES/` in the Windows package. See [licensing boundaries](docs/LICENSE-OPTIONS.md).
