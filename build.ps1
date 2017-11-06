$ErrorActionPreference = 'Stop';
$files = ""
Write-Host Starting build

$node="stefanscherer/node-windows:8.6.0-nanoserver"
docker build -t winspector --build-arg node=$node --build-arg target=$node .
