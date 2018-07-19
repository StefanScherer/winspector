$ErrorActionPreference = 'Stop';
$files = ""
Write-Host Starting build

$node="stefanscherer/node-windows:10.6.0"
docker build -t winspector --build-arg node=$node --build-arg target=$node .
