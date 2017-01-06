$ErrorActionPreference = 'Stop';

if (! (Test-Path Env:\APPVEYOR_REPO_TAG_NAME)) {
  Write-Host "No version tag detected. Skip publishing."
  exit 0
}

Write-Host Starting deploy
docker login -u="$env:DOCKER_USER" -p="$env:DOCKER_PASS"

docker tag winspector stefanscherer/winspector:$env:APPVEYOR_REPO_TAG_NAME
docker tag winspector stefanscherer/winspector:latest

docker push stefanscherer/winspector:$env:APPVEYOR_REPO_TAG_NAME
docker push stefanscherer/winspector:latest
