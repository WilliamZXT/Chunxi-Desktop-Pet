from __future__ import annotations

import argparse
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from PySide6.QtCore import QLockFile, QStandardPaths, QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from .config import CONFIG_PATH, RUNTIME_ROOT, ConfigRecovery, load_config
from .animation import SpriteLibrary
from .config import DESKTOP_ROOT
from .window import PetWindow
from . import __version__


def main():
    parser = argparse.ArgumentParser(description=f"春喜独立桌宠 v{__version__}")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--quit-after", type=float, help="Smoke-test exit timeout in seconds")
    parser.add_argument("--no-persist", action="store_true")
    parser.add_argument("--autostart",action="store_true",help="Started by the opt-in Windows login entry")
    parser.add_argument("--soak-test-seconds",type=float,help="Real elapsed time endurance recording, no time acceleration")
    parser.add_argument("--soak-output",type=Path)
    parser.add_argument("--check", action="store_true", help="Validate config and all sprite resources without opening the pet")
    parser.add_argument("--check-output", type=Path, help="Write the validation result as JSON")
    args = parser.parse_args()
    app = QApplication(sys.argv[:1])
    app.setApplicationName("Chunxi Desktop Pet")
    app.setOrganizationName("Chunxi")
    app.setApplicationVersion(__version__)
    if args.check:
        try:
            recovery = ConfigRecovery()
            config = load_config(args.config, recovery=recovery, repair=False)
            library = SpriteLibrary(DESKTOP_ROOT / "assets/animations.json")
            from PySide6.QtGui import QIcon
            if QIcon(str(DESKTOP_ROOT/'assets/chunxi.ico')).isNull():
                raise ValueError('Application icon is missing or invalid')
            result = {"ok": True, "version": __version__, "clips": len(library.clips),
                      "config_path": str((args.config or CONFIG_PATH).resolve()),
                      "effective_scale": config['window']['scale'],
                      "config_recovery_needed": bool(recovery.issues), "config_warnings": recovery.issues}
        except Exception as error:
            result = {"ok": False, "error": str(error)}
        if args.check_output:
            args.check_output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        if sys.stdout is not None:
            print(json.dumps(result, ensure_ascii=True))
        return 0 if result["ok"] else 1
    lock = QLockFile(str(Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation)) / "chunxi-desktop-pet.lock"))
    if not lock.tryLock(100):
        notice = QMessageBox(QMessageBox.Icon.Information, '春喜', '春喜已经在运行，请在桌面或系统托盘查找。')
        if args.quit_after:
            QTimer.singleShot(round(args.quit_after * 1000), notice.accept)
        notice.exec()
        return 0
    logs = RUNTIME_ROOT / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(logs / "chunxi.log", maxBytes=500_000, backupCount=2, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s %(name)s %(message)s")
    def fatal_error(kind, value, traceback):
        logging.critical("Unhandled runtime exception", exc_info=(kind, value, traceback))
        QMessageBox.critical(None, "春喜运行异常", f"{value}\n\n程序将退出，详情见 {logs / 'chunxi.log'}")
        app.exit(1)
    sys.excepthook = fatal_error
    try:
        recovery = ConfigRecovery()
        config = load_config(args.config, recovery=recovery)
        logging.info('Config source=%s; scale=%s; repaired=%s',
                     'explicit' if args.config else ('user' if getattr(sys, 'frozen', False) else 'source'),
                     config['window']['scale'], recovery.persisted and bool(recovery.issues))
        window = PetWindow(config, persist=not args.no_persist and not args.soak_test_seconds,
                           config_path=args.config or CONFIG_PATH)
        window.show()
        if recovery.issues:
            notice = QMessageBox(window)
            notice.setWindowTitle('春喜 · 配置已安全恢复')
            notice.setIcon(QMessageBox.Icon.Warning)
            text = '\n'.join(recovery.issues)
            if recovery.backup:
                text += f'\n\n原文件备份：\n{recovery.backup}'
            else:
                text += '\n\n修正仅用于本次运行，未覆盖原文件。'
            notice.setText(text)
            notice.setInformativeText('可以先正常使用春喜；右键“打开当前配置文件”查看设置。')
            window._config_notice = notice
            QTimer.singleShot(0, notice.show)
        recorder=None
        if args.soak_test_seconds:
            from .soak import SoakRecorder
            recorder=SoakRecorder(window,args.soak_test_seconds,args.soak_output or RUNTIME_ROOT/'soak-report.json')
            app.aboutToQuit.connect(lambda:recorder.finish(False))
        if args.quit_after:
            QTimer.singleShot(round(args.quit_after*1000), window.close)
        logging.info("Chunxi Desktop Pet v%s started",__version__)
        return app.exec()
    except Exception as error:
        logging.exception("Unable to start Chunxi")
        QMessageBox.critical(None, "春喜启动失败", f"{error}\n\n详细信息见 {logs / 'chunxi.log'}")
        return 1
    finally:
        lock.unlock()


if __name__ == "__main__":
    raise SystemExit(main())
