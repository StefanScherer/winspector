Write-Host Starting test

$ErrorActionPreference = 'Stop';
Write-Host Testing container
docker run --rm winspector microsoft/windowsservercore
docker run --rm winspector mcr.microsoft.com/windows-insider
