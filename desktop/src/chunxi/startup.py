"""Opt-in current-user startup. Never touch the registry during import or tests."""
import subprocess
import sys
from pathlib import Path

from .config import CONFIG_PATH, DESKTOP_ROOT, FROZEN

KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE = "ChunxiDesktopPet"


def command(config_path: Path | None = None) -> str:
    if FROZEN:
        arguments = [sys.executable, "--autostart"]
    else:
        pythonw = Path(sys.executable).with_name("pythonw.exe")
        arguments = [str(pythonw if pythonw.exists() else Path(sys.executable)), str(DESKTOP_ROOT / "run.py"), "--autostart"]
    if config_path is not None and Path(config_path).resolve() != CONFIG_PATH.resolve():
        arguments.extend(['--config', str(Path(config_path).resolve())])
    return subprocess.list2cmdline(arguments)


def is_enabled(config_path: Path | None = None) -> bool:
    if sys.platform != "win32":
        return False
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as key:
            value, kind = winreg.QueryValueEx(key, VALUE)
            return value == command(config_path) and kind == winreg.REG_SZ
    except FileNotFoundError:
        return False


def set_enabled(enabled: bool, config_path: Path | None = None):
    if sys.platform != "win32":
        if enabled:
            raise OSError("Startup is supported only on Windows")
        return
    import winreg
    if enabled:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, KEY) as key:
            winreg.SetValueEx(key, VALUE, 0, winreg.REG_SZ, command(config_path))
    else:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as key:
                winreg.QueryValueEx(key, VALUE)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, VALUE)
        except FileNotFoundError:
            pass
