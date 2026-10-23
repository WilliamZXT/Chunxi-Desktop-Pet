param([ValidatePattern('^[a-zA-Z0-9.-]+$')][string]$Variant = '')
$ErrorActionPreference = 'Stop'
$desktop = Split-Path $PSScriptRoot -Parent
$version = (Get-Content -LiteralPath (Join-Path $desktop 'VERSION') -Raw).Trim()
$buildFolder = if ($Variant) { "v$version-$Variant" } else { "v$version" }
$originalBuildPath = $env:PATH
$originalInstallerCache = $env:PYINSTALLER_CONFIG_DIR
Push-Location $desktop
try {
    $existingExe = Join-Path $desktop "build\dist\$buildFolder\ChunxiDesktopPet\ChunxiDesktopPet.exe"
    if (Test-Path -LiteralPath $existingExe) {
        try { $probe = [System.IO.File]::Open($existingExe, 'Open', 'ReadWrite', 'None'); $probe.Dispose() }
        catch { throw 'Please exit the running Chunxi Desktop Pet before rebuilding its release directory.' }
    }
    $builderVersion = & '.\.venv\Scripts\python.exe' -c "import importlib.util, importlib.metadata; print(importlib.metadata.version('pyinstaller') if importlib.util.find_spec('PyInstaller') else '')"
    if ($builderVersion -ne '6.16.0') {
        & '.\.venv\Scripts\python.exe' -m pip install -r requirements-build.txt
        if ($LASTEXITCODE -ne 0) { throw 'PyInstaller installation failed' }
    }
    $assetData = (Join-Path $desktop 'assets') + ';desktop/assets'
    $configData = (Join-Path $desktop 'config') + ';desktop/config'
    $sharedData = (Join-Path (Split-Path $desktop -Parent) 'shared\sprites') + ';shared/sprites'
    # Keep unrelated PDF/ICU distributions out of native dependency discovery.
    # Qt uses Windows' ICU API; a Poppler ICU DLL with the same name is incompatible.
    $env:PATH = (Join-Path $desktop '.venv\Scripts') + ';' + $env:SystemRoot + '\System32;' + $env:SystemRoot
    $env:PYINSTALLER_CONFIG_DIR = Join-Path $PSScriptRoot 'pyinstaller-cache'
    & '.\.venv\Scripts\python.exe' -m PyInstaller --noconfirm --clean --windowed --onedir --name ChunxiDesktopPet --icon (Join-Path $desktop 'assets/chunxi.ico') --version-file (Join-Path $PSScriptRoot 'windows-version.txt') --paths (Join-Path $desktop 'src') --add-data $assetData --add-data $configData --add-data $sharedData --distpath "build/dist/$buildFolder" --workpath "build/work/$buildFolder" --specpath "build/spec/$buildFolder" (Join-Path $desktop 'run.py')
    if ($LASTEXITCODE -ne 0) { throw 'EXE build failed' }
    & '.\.venv\Scripts\python.exe' (Join-Path $PSScriptRoot 'finalize_distribution.py') --destination (Split-Path $existingExe -Parent)
    if ($LASTEXITCODE -ne 0) { throw 'Distribution finalization failed' }
} finally { $env:PATH = $originalBuildPath; $env:PYINSTALLER_CONFIG_DIR = $originalInstallerCache; Pop-Location }
