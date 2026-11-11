param(
    [string]$ToolRoot = 'D:\RespawnTools',
    [string]$JdkHome,
    [switch]$UseWindowsTrustStore
)
$ErrorActionPreference = 'Stop'
if (-not $JdkHome) {
    $jdkFolder = Get-ChildItem -LiteralPath (Join-Path $ToolRoot 'jdk21') -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'bin\jlink.exe') } |
        Sort-Object Name -Descending | Select-Object -First 1
    if (-not $jdkFolder) { throw 'Pun JDK nije pronadjen. Prosledi -JdkHome.' }
    $JdkHome = $jdkFolder.FullName
}
if (-not (Test-Path -LiteralPath (Join-Path $JdkHome 'bin\jlink.exe'))) {
    throw 'JdkHome mora da pokazuje na pun JDK sa jlink alatom.'
}
$sdkRoot = Join-Path $ToolRoot 'android-sdk'
if (-not (Test-Path -LiteralPath (Join-Path $sdkRoot 'platform-tools\adb.exe'))) {
    throw 'Android SDK nije instaliran u izabranom ToolRoot direktorijumu.'
}
$env:JAVA_HOME = $JdkHome
$env:ANDROID_HOME = $sdkRoot
$env:ANDROID_SDK_ROOT = $sdkRoot
$env:ANDROID_AVD_HOME = Join-Path $ToolRoot 'avd'
$env:ANDROID_USER_HOME = Join-Path $ToolRoot 'android-user'
$env:GRADLE_USER_HOME = Join-Path $ToolRoot 'gradle'
if ($UseWindowsTrustStore) {
    $env:JAVA_TOOL_OPTIONS = ($env:JAVA_TOOL_OPTIONS + ' -Djavax.net.ssl.trustStoreType=Windows-ROOT -Djavax.net.ssl.trustStore=NONE').Trim()
}
Write-Output "JAVA_HOME: $JdkHome"
Write-Output "ANDROID_HOME: $sdkRoot"
