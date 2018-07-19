#!/bin/bash
set -e

echo Testing container
docker run --rm winspector microsoft/windowsservercore
docker run --rm winspector mcr.microsoft.com/windows-insider
