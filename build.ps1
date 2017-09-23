$ErrorActionPreference = 'Stop';
$files = ""
Write-Host Starting build

Write-Host Preinstalled images
docker images

# Write-Host Updating base images
# docker pull microsoft/windowsservercore
# docker pull microsoft/nanoserver

docker build -t winspector -f Dockerfile.windows .

docker images
