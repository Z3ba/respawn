param([Parameter(ValueFromRemainingArguments = $true)][string[]]$FlutterArguments)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$flutterExecutable = Join-Path $projectRoot '.tools\flutter\bin\flutter.bat'
if (-not (Test-Path -LiteralPath $flutterExecutable)) {
    throw 'Lokalni Flutter SDK nije instaliran. Instaliraj Flutter stable i koristi flutter iz PATH-a.'
}
$env:PUB_CACHE = Join-Path $projectRoot '.tools\pub-cache'
$env:CI = 'true'
$env:FLUTTER_SUPPRESS_ANALYTICS = 'true'
Push-Location (Split-Path -Parent $flutterExecutable)
try {
    # Flutter native hooks on Windows currently require an SDK path without spaces.
    $flutterShortDirectory = (cmd /c 'for %I in (.) do @echo %~sI').Trim()
    $flutterExecutable = Join-Path $flutterShortDirectory 'flutter.bat'
}
finally { Pop-Location }
Push-Location (Join-Path $projectRoot 'mobile')
try { & $flutterExecutable @FlutterArguments; exit $LASTEXITCODE }
finally { Pop-Location }
