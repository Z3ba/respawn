param(
    [string]$ToolRoot = 'D:\RespawnTools',
    [Parameter(Mandatory = $true)][string]$JavaHome,
    [switch]$AcceptSdkLicense,
    [switch]$IncludeEmulator,
    [switch]$UseWindowsTrustStore
)
$ErrorActionPreference = 'Stop'

# This script is opt-in. Review the Android SDK terms before supplying the flag:
# https://developer.android.com/studio#terms-and-conditions
if (-not $AcceptSdkLicense) {
    throw 'Prvo pregledaj Android SDK licencu. Instalacija zahteva izricit -AcceptSdkLicense.'
}
if (-not (Test-Path -LiteralPath (Join-Path $JavaHome 'bin\javac.exe'))) {
    throw 'JavaHome mora da pokazuje na JDK 17+ sa javac alatom.'
}
$compilerVersion = (& (Join-Path $JavaHome 'bin\javac.exe') -version 2>&1 | Out-String)
if ($compilerVersion -notmatch 'javac (\d+)' -or [int]$Matches[1] -lt 17) {
    throw 'Potreban je JDK 17 ili noviji; preporucen je JDK 21.'
}
if (-not (Test-Path -LiteralPath (Join-Path $JavaHome 'bin\jlink.exe'))) {
    throw 'Potreban je pun JDK sa jlink alatom; Eclipse JRE nije dovoljan.'
}
if ($UseWindowsTrustStore) {
    $env:JAVA_TOOL_OPTIONS = ($env:JAVA_TOOL_OPTIONS + ' -Djavax.net.ssl.trustStoreType=Windows-ROOT -Djavax.net.ssl.trustStore=NONE').Trim()
}
if (-not [System.IO.Path]::IsPathRooted($ToolRoot)) {
    throw 'ToolRoot mora biti apsolutna putanja.'
}
$sdkRoot = Join-Path $ToolRoot 'android-sdk'
$toolsRoot = Join-Path $sdkRoot 'cmdline-tools\latest'
$archive = Join-Path $ToolRoot 'android-commandline-tools.zip'
$download = 'https://dl.google.com/android/repository/commandlinetools-win-15859902_latest.zip'
$expectedHash = '90ae805d20434428bffcb699c290860f19bb5f66a67e6b330067e3de801fb04a'
New-Item -ItemType Directory -Force $ToolRoot | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $toolsRoot 'bin\sdkmanager.bat'))) {
    if (Test-Path -LiteralPath $toolsRoot) {
        throw 'Ciljni cmdline-tools/latest vec postoji, ali nije kompletan. Ne prepisujem ga.'
    }
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $download -OutFile $archive
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne $expectedHash) {
        throw 'Android command-line tools SHA256 provera nije uspela.'
    }
    $staging = Join-Path $ToolRoot 'android-cli-staging'
    if (Test-Path -LiteralPath $staging) { throw 'Staging direktorijum vec postoji.' }
    Expand-Archive -LiteralPath $archive -DestinationPath $staging
    New-Item -ItemType Directory -Force (Split-Path -Parent $toolsRoot) | Out-Null
    # Verify exact task-owned paths before moving the new tool directory.
    $source = (Resolve-Path -LiteralPath (Join-Path $staging 'cmdline-tools')).Path
    $destination = [System.IO.Path]::GetFullPath($toolsRoot)
    $allowedRoot = [System.IO.Path]::GetFullPath($ToolRoot).TrimEnd('\') + '\'
    if (-not $source.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase) -or
        -not $destination.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Putanje alata izlaze iz izabranog ToolRoot direktorijuma.'
    }
    Move-Item -LiteralPath $source -Destination $destination
    Remove-Item -LiteralPath $archive
}
$env:JAVA_HOME = $JavaHome
$env:ANDROID_HOME = $sdkRoot
$env:ANDROID_SDK_ROOT = $sdkRoot
$env:ANDROID_AVD_HOME = Join-Path $ToolRoot 'avd'
$env:ANDROID_USER_HOME = Join-Path $ToolRoot 'android-user'
$env:GRADLE_USER_HOME = Join-Path $ToolRoot 'gradle'
$manager = Join-Path $toolsRoot 'bin\sdkmanager.bat'
$packages = @('platform-tools', 'platforms;android-36', 'platforms;android-35', 'build-tools;36.0.0', 'cmake;3.22.1', 'ndk;28.2.13676358')
if ($IncludeEmulator) {
    $packages += @('emulator', 'system-images;android-35;default;x86_64')
}
1..50 | ForEach-Object { 'y' } | & $manager "--sdk_root=$sdkRoot" @packages
if ($LASTEXITCODE -ne 0) { throw 'Instalacija Android paketa nije uspela.' }
Write-Output "Android SDK: $sdkRoot"
Write-Output "GRADLE_USER_HOME: $env:GRADLE_USER_HOME"
Write-Output 'Globalni PATH i postojece Java instalacije nisu menjani.'
