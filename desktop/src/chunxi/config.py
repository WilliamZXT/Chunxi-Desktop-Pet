from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import logging
import math
import os
from pathlib import Path
import shutil
import sys
import tempfile

FROZEN = getattr(sys, 'frozen', False)
PROJECT_ROOT = Path(sys._MEIPASS) if FROZEN else Path(__file__).resolve().parents[3]
DESKTOP_ROOT = PROJECT_ROOT / 'desktop'
RUNTIME_ROOT = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'ChunxiDesktopPet' if FROZEN else DESKTOP_ROOT / 'build'
CONFIG_PATH = RUNTIME_ROOT / 'config.json'
# Existing supported window/poll limits, shared with the size UI.
MIN_SCALE, MAX_SCALE = 0.5, 3.0
RANGE_KEYS = ('loaf_after_seconds', 'sleep_after_seconds', 'blink_interval_seconds',
              'ear_interval_seconds', 'look_cooldown_seconds', 'click_cooldown_seconds')
log = logging.getLogger(__name__)


@dataclass
class ConfigRecovery:
    issues: list[str] = field(default_factory=list)
    backup: Path | None = None
    persisted: bool = False


def _number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def _read_json(path):
    def reject_constant(value):
        raise ValueError('Non-finite number in JSON')
    return json.loads(path.read_text(encoding='utf-8-sig'), parse_constant=reject_constant)


def _atomic_write(path: Path, config: dict):
    # Serialize first: invalid data must never truncate a working configuration.
    text = json.dumps(config, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _backup(path):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = path.with_name(path.name + '.' + stamp + '.bak')
    # copy2 preserves the original bytes, including invalid JSON and encoding.
    shutil.copy2(path, backup)
    return backup


def _normalize(defaults, overrides, issues):
    config = copy.deepcopy(defaults)
    if not isinstance(overrides, dict):
        issues.append('配置根节点应为 JSON 对象，已使用默认配置。')
        overrides = {}
    for key, value in overrides.items():
        if key in ('window', 'behavior', 'interaction', 'preferences'):
            if not isinstance(value, dict):
                issues.append(f'{key} 应为对象，已仅恢复该部分默认值。')
                continue
            config[key].update(value)
        else:
            config[key] = value

    def fallback(section, key):
        config[section][key] = copy.deepcopy(defaults[section][key])
        issues.append(f'{section}.{key} 类型或数值不合法，已仅恢复此参数默认值。')

    def bounded(section, key, low, high=None, integer=False):
        value = config[section][key]
        if not _number(value) or (integer and int(value) != value):
            fallback(section, key)
            return
        fixed = max(low, value) if high is None else max(low, min(high, value))
        if fixed != value:
            issues.append(f'{section}.{key} 超出支持范围，已修正为 {fixed}。')
        config[section][key] = int(fixed) if integer else fixed

    bounded('window', 'scale', MIN_SCALE, MAX_SCALE)
    if type(config['window']['always_on_top']) is not bool:
        fallback('window', 'always_on_top')
    position = config['window'].get('position')
    if position is not None and not (isinstance(position, list) and len(position) == 2 and all(type(v) is int and -(2**31) <= v < 2**31 for v in position)):
        fallback('window', 'position')
    for key in RANGE_KEYS:
        value = config['behavior'][key]
        if not isinstance(value, list) or len(value) != 2 or not all(_number(v) and v > 0 for v in value):
            fallback('behavior', key)
        elif value[0] > value[1]:
            config['behavior'][key] = sorted(value)
            issues.append(f'behavior.{key} 的上下限顺序已修正。')
    behavior = config['behavior']
    if behavior['sleep_after_seconds'][0] <= behavior['loaf_after_seconds'][1]:
        # Preserve loaf preference and move only the incompatible sleep threshold.
        lower = math.nextafter(float(behavior['loaf_after_seconds'][1]), math.inf)
        if not math.isfinite(lower):
            fallback('behavior', 'loaf_after_seconds')
            lower = math.nextafter(float(behavior['loaf_after_seconds'][1]), math.inf)
        old = behavior['sleep_after_seconds']
        behavior['sleep_after_seconds'] = [max(lower, old[0]), max(lower, old[1])]
        issues.append('打盹时间必须晚于猫饼时间，已仅延后打盹阈值。')
    for key in ('look_probability', 'click_probability'):
        bounded('behavior', key, 0, 1)
    for key in ('near_radius_pixels', 'wake_seconds'):
        value = behavior[key]
        if not _number(value) or value <= 0:
            fallback('behavior', key)
    bounded('interaction', 'poll_ms', 20, 2000, integer=True)
    for key in ('mouse_move_threshold_pixels', 'drag_threshold_pixels'):
        value = config['interaction'][key]
        if not _number(value) or value <= 0 or int(value) != value:
            fallback('interaction', key)
        else:
            config['interaction'][key] = int(value)
    if config['preferences']['frequency'] not in ('quiet', 'normal', 'more'):
        fallback('preferences', 'frequency')
    config['version'] = '0.1.1'
    return config


def load_config(path: Path | None = None, *, recovery: ConfigRecovery | None = None, repair=True) -> dict:
    defaults = _read_json(DESKTOP_ROOT / 'config/default.json')
    validate_config(defaults)
    source = Path(path) if path is not None else CONFIG_PATH
    report = recovery if recovery is not None else ConfigRecovery()
    existed = source.exists()
    raw = None
    read_ok = False
    parse_error = False
    if existed:
        try:
            raw = _read_json(source)
            read_ok = True
        except (ValueError, UnicodeError):
            parse_error = True
            report.issues.append('配置文件格式或编码损坏，已使用默认配置；原文件将保留备份。')
        except OSError:
            report.issues.append('无法读取配置文件，本次使用默认配置；原文件未覆盖。')
    config = _normalize(defaults, raw if read_ok else {}, report.issues)
    validate_config(config)
    # Missing fields are supplied in memory. A valid user file is never rewritten on load.
    should_write = repair and (not existed or bool(report.issues) and (read_ok or parse_error))
    if should_write:
        try:
            if existed:
                # If backup fails, do not touch the original file.
                report.backup = _backup(source)
            _atomic_write(source, config)
            report.persisted = True
        except OSError:
            report.issues.append('无法备份或保存修复配置，本次使用内存中的安全值，原设置未被主动覆盖。')
    for issue in report.issues:
        log.warning('%s', issue)
    return config


def validate_config(config: dict):
    if not isinstance(config, dict):
        raise ValueError('Configuration must be a JSON object')
    for section in ('window', 'behavior', 'interaction', 'preferences'):
        if not isinstance(config.get(section), dict):
            raise ValueError(f'Invalid section: {section}')
    behavior = config['behavior']
    for key in RANGE_KEYS:
        bounds = behavior.get(key)
        if not isinstance(bounds, list) or len(bounds) != 2 or not all(_number(v) for v in bounds) or not 0 < bounds[0] <= bounds[1]:
            raise ValueError(f'Invalid time range: {key}')
    if behavior['sleep_after_seconds'][0] <= behavior['loaf_after_seconds'][1]:
        raise ValueError('Sleep threshold must be later than loaf threshold')
    for key in ('look_probability', 'click_probability'):
        if not _number(behavior.get(key)) or not 0 <= behavior[key] <= 1:
            raise ValueError(f'Invalid probability: {key}')
    scale = config['window'].get('scale')
    if not _number(scale) or not MIN_SCALE <= scale <= MAX_SCALE:
        raise ValueError('Window scale must be between 0.5 and 3')
    if type(config['window'].get('always_on_top')) is not bool:
        raise ValueError('always_on_top must be boolean')
    position = config['window'].get('position')
    if position is not None and not (isinstance(position, list) and len(position) == 2 and all(type(v) is int and -(2**31) <= v < 2**31 for v in position)):
        raise ValueError('Invalid position')
    poll = config['interaction'].get('poll_ms')
    if type(poll) is not int or not 20 <= poll <= 2000:
        raise ValueError('Polling interval must be an integer between 20 and 2000 ms')
    for key in ('wake_seconds', 'near_radius_pixels'):
        if not _number(behavior.get(key)) or behavior[key] <= 0:
            raise ValueError(f'{key} must be positive')
    for key in ('mouse_move_threshold_pixels', 'drag_threshold_pixels'):
        value = config['interaction'].get(key)
        if type(value) is not int or value <= 0:
            raise ValueError(f'{key} must be a positive integer')
    if config['preferences'].get('frequency') not in ('quiet', 'normal', 'more'):
        raise ValueError('Unknown behavior frequency')


def save_config(config: dict, path: Path | None = None):
    validate_config(config)
    target = Path(path) if path is not None else CONFIG_PATH
    # Also preserve existing preferences before an explicit UI save.
    if target.exists():
        _backup(target)
    _atomic_write(target, config)
