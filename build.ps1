$ErrorActionPreference = 'Stop';
$files = ""
Write-Host Starting build

$node="stefanscherer/node-windows:10.7.0"
docker build -t winspector --build-arg node=$node --build-arg target=$node .
