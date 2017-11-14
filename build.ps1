$ErrorActionPreference = 'Stop';
$files = ""
Write-Host Starting build

$node="stefanscherer/node-windows:8.9.1-nanoserver"
docker build -t winspector --build-arg node=$node --build-arg target=$node .
