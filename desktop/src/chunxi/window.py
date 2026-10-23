from __future__ import annotations

import json
import copy
import logging
import math
import time
from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, QTimer, Qt, QUrl
from PySide6.QtGui import QAction, QBitmap, QDesktopServices, QIcon, QImage, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QApplication, QDialog, QMenu, QMessageBox, QSystemTrayIcon, QWidget

from .animation import Animator, SpriteLibrary
from .config import CONFIG_PATH, DESKTOP_ROOT, RUNTIME_ROOT, save_config
from .display import visible_position
from .settings import SettingsDialog, SizeDialog
from . import __version__, startup
from .interaction import ActivityMonitor, DragGesture, direction_for
from .state_machine import PetStateMachine, State

log = logging.getLogger(__name__)


class PetWindow(QWidget):
    def __init__(self, config: dict, *, persist: bool = True, rng=None, config_path=None):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowDoesNotAcceptFocus
        if config["window"]["always_on_top"]:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        super().__init__(None, flags)
        self.setWindowTitle(f"春喜 · Chunxi Desktop Pet v{__version__}")
        self.setWindowIcon(QIcon(str(DESKTOP_ROOT / 'assets/chunxi.ico')))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)
        self.config, self.persist = config, persist
        self.config_path = (Path(config_path) if config_path is not None else CONFIG_PATH).resolve()
        scale = config["window"]["scale"]
        self.setFixedSize(round(192*scale), round(208*scale))
        now = time.monotonic()
        self.library = SpriteLibrary(DESKTOP_ROOT / "assets/animations.json")
        self.machine = PetStateMachine(config["behavior"], now, rng)
        self.machine.set_frequency(config['preferences']['frequency'],now)
        self.animator = Animator(self.library, now)
        self.monitor = ActivityMonitor(config["interaction"]["mouse_move_threshold_pixels"])
        self.gesture = DragGesture(config["interaction"]["drag_threshold_pixels"])
        self._display_frame = self.animator.frame(now)
        self._paint_key = None
        self._last_state = self.machine.state
        self._last_poll = now
        self._last_mask = None
        self._closing = False
        self._restore_position()
        self.menu = self._make_menu()
        self.tray = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self.windowIcon(), self)
            self.tray.setToolTip("春喜 · 安静陪伴（右键可退出）")
            self.tray.setContextMenu(self.menu)
            self.tray.show()
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.setInterval(33)
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        app=QApplication.instance()
        app.screenRemoved.connect(self._screen_removed)
        app.screenAdded.connect(self._connect_screen)
        for screen in app.screens():
            self._connect_screen(screen)
        self._tick()

    def _make_menu(self):
        menu = QMenu(self)
        title = menu.addAction(f"春喜 · Desktop v{__version__}")
        title.setEnabled(False)
        pause = QAction("暂停自动行为", self, checkable=True)
        self.pause_action = pause
        pause.toggled.connect(self._set_paused)
        menu.addAction(pause)
        menu.addAction("回到屏幕右下方", self.reset_position)
        menu.addAction("调节大小…", self.open_size)
        menu.addAction("设置…", self.open_settings)
        menu.addAction("打开当前配置文件", self.open_config)
        menu.addAction("配置参数说明", self.open_config_help)
        menu.addAction("打开日志文件夹", lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(RUNTIME_ROOT / "logs"))))
        menu.addSeparator()
        menu.addAction("退出春喜", self.close)
        return menu

    def _set_paused(self, value):
        self.machine.set_paused(value, time.monotonic())
        self.pause_action.setText('恢复自动行为（当前已暂停）' if value else '暂停自动行为')
        self.setWindowTitle(f"春喜 · Chunxi Desktop Pet v{__version__}" + (' · 已暂停' if value else ''))
        if self.tray:
            self.tray.setToolTip('春喜 · 已暂停自动行为' if value else '春喜 · 安静陪伴（右键可退出）')

    def open_config(self):
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.config_path.resolve()))):
            QMessageBox.warning(self, '春喜配置', f'无法打开配置文件，请手动打开：\n{self.config_path}')

    def open_config_help(self):
        QMessageBox.information(self, '春喜 · 配置说明',
            '优先使用“调节大小…”或“设置…”修改常用参数。\n\n'
            'scale：0.5–3.0；0.8 表示 80%。\n'
            '概率：0–1；时间范围：[最短秒数, 最长秒数]，必须为正数且按顺序排列。\n'
            '打盹最短时间必须晚于猫饼最长时间。poll_ms：20–2000 毫秒。\n'
            'frequency：quiet / normal / more。\n\n'
            '手动修改后需重启；修复错误配置前会先备份原文件。')

    def open_size(self):
        original = self.config['window']['scale']
        original_position = self.pos()
        dialog = SizeDialog(original, self)
        dialog.size.valueChanged.connect(lambda percent: self._apply_size(percent / 100))
        try:
            if dialog.exec() != QDialog.DialogCode.Accepted:
                self._apply_size(original)
                self.move(original_position)
                self._keep_visible()
                return
            config = copy.deepcopy(self.config)
            config['window']['scale'] = dialog.size.value() / 100
            save_config(config, self.config_path)
            self.config = config
            self._apply_size(config['window']['scale'])
        except Exception as error:
            self._apply_size(original)
            self.move(original_position)
            self._keep_visible()
            log.exception('Size could not be saved')
            QMessageBox.warning(self, '春喜大小', f'大小未能保存，已恢复原大小：{error}')

    def _apply_size(self, scale):
        anchor = self.geometry().bottomLeft()
        self.setFixedSize(round(192 * scale), round(208 * scale))
        self.move(anchor.x(), anchor.y() - self.height() + 1)
        self._paint_key = None
        self._keep_visible()
        self._tick()

    def open_settings(self):
        try:
            was_enabled=startup.is_enabled(self.config_path)
            dialog=SettingsDialog(self.config,was_enabled,self)
            if dialog.exec()!=QDialog.DialogCode.Accepted:
                return
            config=dialog.selected_config()
            desired=dialog.startup.isChecked()
            changed=desired!=was_enabled
            # Saving is explicit consent: also remove stale entries after a move,
            # or refresh an enabled entry to the current executable location.
            startup.set_enabled(desired, self.config_path)
            try:
                save_config(config, self.config_path)
            except Exception:
                if changed:
                    startup.set_enabled(was_enabled, self.config_path)
                raise
            self.apply_preferences(config)
        except Exception as error:
            log.exception('Settings could not be saved')
            QMessageBox.warning(self,'春喜设置',f'设置未能保存：{error}')

    def apply_preferences(self, config):
        anchor=self.geometry().bottomLeft()
        self.config=config
        scale=config['window']['scale']
        self.setFixedSize(round(192*scale),round(208*scale))
        position=self.pos()
        position.setY(anchor.y()-self.height()+1)
        self.move(position)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,config['window']['always_on_top'])
        self.show()
        self.machine.set_frequency(config['preferences']['frequency'],time.monotonic())
        self._paint_key=None
        self._keep_visible()
        self._tick()

    def _connect_screen(self, screen):
        screen.availableGeometryChanged.connect(self._display_changed)
        screen.logicalDotsPerInchChanged.connect(self._display_changed)

    def _screen_removed(self, screen):
        QTimer.singleShot(150,self._keep_visible)

    def _display_changed(self, *args):
        self._paint_key=None
        if not self.gesture.dragging:
            self._keep_visible()

    def _keep_visible(self):
        if self._closing:
            return
        self.move(visible_position(self.pos(),self.size(),[s.availableGeometry() for s in QApplication.screens()]))

    def event(self,event):
        if event.type()==QEvent.Type.DevicePixelRatioChange and hasattr(self,'_paint_key'):
            self._paint_key=None
        return super().event(event)

    def reset_position(self):
        rect = QApplication.primaryScreen().availableGeometry()
        self.move(rect.right()-self.width()-48, rect.bottom()-self.height()-24)

    def _restore_position(self):
        position = self.config["window"].get("position")
        saved = RUNTIME_ROOT / "runtime-state.json"
        if self.persist and saved.exists():
            try:
                position = json.loads(saved.read_text(encoding="utf-8"))["position"]
            except (ValueError, OSError, KeyError, TypeError):
                log.warning("Ignoring unreadable saved window position")
        if isinstance(position, list) and len(position) == 2 and all(type(v) is int and -(2**31) <= v < 2**31 for v in position):
            self.move(*position)
            self._keep_visible()
            return
        self.reset_position()

    def _tick(self):
        now = time.monotonic()
        if now-self._last_poll >= self.config["interaction"]["poll_ms"]/1000:
            self._last_poll = now
            active, cursor = self.monitor.poll()
            if active:
                self.machine.activity(now)
            center = self.frameGeometry().center()
            distance = math.hypot(cursor.x()-center.x(), cursor.y()-center.y())
            near = 1 < distance <= self.config["behavior"]["near_radius_pixels"]
            self.machine.proximity(now, near, direction_for(cursor, center))
        self.machine.tick(now)
        key, direction = self.machine.clip_key, self.machine.look_direction
        if key != self.animator.key or (key == "look" and direction != self.animator.direction):
            self.animator.select(key, direction, now)
        self._last_state = self.machine.state
        frame = self.render_frame(now)
        paint_key=(frame.cacheKey(),self.width(),self.height(),self.devicePixelRatioF())
        if paint_key!=self._paint_key:
            self._display_frame=frame
            scaled = frame.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
            mask = QRegion(QBitmap.fromImage(scaled.createAlphaMask()))
            if mask != self._last_mask:
                self.setMask(mask)
                self._last_mask = mask
            self._paint_key=paint_key
            self.update()

    def render_frame(self, now: float) -> QImage:
        # Atomic whole-frame replacement: no additive blend or partial-opacity body.
        return self.animator.frame(now)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.drawImage(self.rect(), self._display_frame)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.gesture.press(event.globalPosition().toPoint(), self.pos())
            self.machine.activity(time.monotonic())
            event.accept()

    def mouseMoveEvent(self, event):
        position = self.gesture.move(event.globalPosition().toPoint())
        if position is not None:
            if self.machine.state != State.DRAGGING:
                self.machine.drag_start(time.monotonic())
            self.move(position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.gesture.release():
                self.machine.drag_end(time.monotonic())
                self._keep_visible()
            else:
                self.machine.click(time.monotonic())
            event.accept()

    def contextMenuEvent(self, event):
        self.menu.exec(event.globalPos())

    def closeEvent(self, event):
        if not self._closing:
            self._closing = True
            self.timer.stop()
            if self.tray:
                self.tray.hide()
            app=QApplication.instance()
            try:
                app.screenRemoved.disconnect(self._screen_removed)
                app.screenAdded.disconnect(self._connect_screen)
                for screen in app.screens():
                    screen.availableGeometryChanged.disconnect(self._display_changed)
                    screen.logicalDotsPerInchChanged.disconnect(self._display_changed)
            except (RuntimeError,TypeError):
                pass
            if self.persist:
                try:
                    path = RUNTIME_ROOT / "runtime-state.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    temporary = path.with_suffix(".tmp")
                    temporary.write_text(json.dumps({"position": [self.x(), self.y()]}), encoding="utf-8")
                    temporary.replace(path)
                except OSError:
                    log.exception("Unable to save window position")
            log.info("Window closed")
        event.accept()
        QApplication.instance().quit()
