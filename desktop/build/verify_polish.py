"""Real Windows EXE checks, isolated from the user's running pet and preferences."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid
import zipfile

desktop = Path(__file__).resolve().parents[1]
qa = desktop / 'build/qa/polish'
qa.mkdir(parents=True, exist_ok=True)
distribution = desktop / 'build/dist/v0.1.1-polish/ChunxiDesktopPet'
run_root = qa / ('clean extract ' + uuid.uuid4().hex[:8])
run_root.mkdir()
archive_path = run_root / 'candidate.zip'
with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in distribution.rglob('*'):
        if path.is_file():
            archive.write(path, Path('春喜 portable') / path.relative_to(distribution))
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None
    archive.extractall(run_root)
portable = run_root / '春喜 portable'
exe = portable / 'ChunxiDesktopPet.exe'
temp = run_root / 'isolated temp'
userdata = run_root / 'isolated appdata'
temp.mkdir()
userdata.mkdir()
env = dict(os.environ, LOCALAPPDATA=str(userdata), TEMP=str(temp), TMP=str(temp), QT_QPA_PLATFORM='windows')
profile = json.loads((desktop / 'config/chunxi-preferences.json').read_text(encoding='utf-8'))
config_path = userdata / 'ChunxiDesktopPet/config.json'
config_path.parent.mkdir()
report = {'scope': 'Real Windows packaged EXE; clean ZIP extraction; isolated appdata and TEMP; no user config changes.',
          'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'errors': [],
          'exe_sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}

def write_config(data):
    config_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

def run(*args, expected=0):
    result = subprocess.run([str(exe), *map(str, args)], cwd=run_root, env=env, timeout=25)
    assert result.returncode == expected, (args, result.returncode)

def check(label):
    report['checks'].append(label)
    print(label, flush=True)

def wait_started(process, baseline):
    log = config_path.parent / 'logs/chunxi.log'
    end = time.monotonic() + 12
    while time.monotonic() < end:
        assert process.poll() is None, 'Process exited before startup'
        if log.exists() and log.read_text(encoding='utf-8').count('started') > baseline:
            return
        time.sleep(.1)
    raise AssertionError('No startup log before timeout')

def start_count():
    log = config_path.parent / 'logs/chunxi.log'
    return log.read_text(encoding='utf-8').count('started') if log.exists() else 0

try:
    write_config(profile)
    original = config_path.read_bytes()
    output = run_root / 'check.json'
    run('--check', '--check-output', output)
    checked = json.loads(output.read_text(encoding='utf-8'))
    assert checked['ok'] and checked['effective_scale'] == .8 and not checked['config_recovery_needed']
    assert Path(checked['config_path']) == config_path
    assert config_path.read_bytes() == original
    check('clean-extraction-dependencies-resources-and-80-percent-path')
    for _ in range(2):
        run('--quit-after', '2', '--no-persist')
    check('normal-start-exit-restart')
    assert config_path.read_bytes() == original
    check('valid-preferences-preserved-without-rewrite')
    bad = json.loads(json.dumps(profile))
    bad['window']['scale'] = 6.0
    write_config(bad)
    raw = config_path.read_bytes()
    run('--quit-after', '2', '--no-persist')
    fixed = json.loads(config_path.read_text(encoding='utf-8'))
    assert fixed['window']['scale'] == 3 and fixed['behavior'] == profile['behavior']
    assert any(p.read_bytes() == raw for p in config_path.parent.glob('config.json.*.bak'))
    check('scale-6-recovery-with-original-backup-and-other-preferences-intact')
    config_path.write_bytes(b'{"window":')
    run('--quit-after', '2', '--no-persist')
    assert isinstance(json.loads(config_path.read_text(encoding='utf-8')), dict)
    assert any(p.read_bytes() == b'{"window":' for p in config_path.parent.glob('config.json.*.bak'))
    check('invalid-json-real-window-recovery-and-exit')
    write_config(profile)
    baseline = start_count()
    first = subprocess.Popen([str(exe), '--quit-after', '6', '--no-persist'], cwd=run_root, env=env)
    try:
        wait_started(first, baseline)
        run('--quit-after', '1', '--no-persist')
        assert first.wait(timeout=15) == 0
        assert start_count() == baseline + 1
    finally:
        if first.poll() is None:
            first.terminate(); first.wait(timeout=10)
    check('duplicate-start-only-one-pet-window-starts')
    baseline = start_count()
    process = subprocess.Popen([str(exe), '--quit-after', '30', '--no-persist'], cwd=run_root, env=env)
    try:
        wait_started(process, baseline)
        process.terminate()
        process.wait(timeout=10)
    finally:
        if process.poll() is None:
            process.terminate(); process.wait(timeout=10)
    run('--quit-after', '2', '--no-persist')
    check('forced-termination-stale-lock-recovery-and-restart')
    sprite = portable / '_internal/shared/sprites/dozing.png'
    hidden = sprite.with_suffix('.missing-test')
    sprite.rename(hidden)
    try:
        run('--check', '--check-output', output, expected=1)
        assert not json.loads(output.read_text(encoding='utf-8'))['ok']
    finally:
        hidden.rename(sprite)
    check('missing-resource-detected-with-exit-code-1')
except Exception as error:
    report['errors'].append(repr(error))
report['ok'] = not report['errors']
report['finished_utc'] = datetime.now(timezone.utc).isoformat()
(qa / 'exe-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
raise SystemExit(0 if report['ok'] else 1)
