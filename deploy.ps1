$ErrorActionPreference = 'Stop';

if (! (Test-Path Env:\APPVEYOR_REPO_TAG_NAME)) {
  Write-Host "No version tag detected. Skip publishing."
  exit 0
}

Write-Host Starting deploy
docker login -u="$env:DOCKER_USER" -p="$env:DOCKER_PASS"

docker tag winspector stefanscherer/winspector:windows-$env:APPVEYOR_REPO_TAG_NAME-2016

docker push stefanscherer/winspector:windows-$env:APPVEYOR_REPO_TAG_NAME-2016

npm install -g rebase-docker-image
rebase-docker-image stefanscherer/winspector:windows-$version-2016 -t stefanscherer/winspector:windows-$version-1709 -b microsoft/nanoserver:1709
