$ErrorActionPreference = 'Stop';

if (! (Test-Path Env:\APPVEYOR_REPO_TAG_NAME)) {
  Write-Host "No version tag detected. Skip publishing."
  exit 0
}

Write-Host Starting deploy
"$env:DOCKER_PASS" | docker login --username "$env:DOCKER_USER" --password-stdin

$version = $env:APPVEYOR_REPO_TAG_NAME

docker tag winspector stefanscherer/winspector:windows-$version-2016
docker push stefanscherer/winspector:windows-$version-2016

npm install -g rebase-docker-image
rebase-docker-image stefanscherer/winspector:windows-$version-2016 `
  -t stefanscherer/winspector:windows-$version-1709 `
  -b microsoft/nanoserver:1709_KB4056892

rebase-docker-image stefanscherer/winspector:windows-$version-2016 `
  -s microsoft/nanoserver:10.0.14393.2068 `
  -t stefanscherer/winspector:windows-$version-insider-17093 `
  -b microsoft/nanoserver-insider:10.0.17093.1000
