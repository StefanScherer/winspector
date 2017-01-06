#!/bin/bash
set -e

echo Testing container
docker run --rm winspector microsoft/windowsservercore
