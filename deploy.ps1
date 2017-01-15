$ErrorActionPreference = 'Stop';

if (! (Test-Path Env:\APPVEYOR_REPO_TAG_NAME)) {
  Write-Host "No version tag detected. Skip publishing."
  exit 0
}

Write-Host Starting deploy
docker login -u="$env:DOCKER_USER" -p="$env:DOCKER_PASS"

docker tag winspector stefanscherer/winspector:windows-$env:APPVEYOR_REPO_TAG_NAME

docker push stefanscherer/winspector:windows-$env:APPVEYOR_REPO_TAG_NAME
