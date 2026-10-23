$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
        py -3.12 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Python virtual environment creation failed. Install Python 3.12 first.' }
    }
    & '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    Write-Host 'Ready. Double-click Start-Chunxi.cmd.'
} finally { Pop-Location }
