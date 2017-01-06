#!/bin/bash
set -e

docker tag winspector stefanscherer/winspector:linux-$TRAVIS_TAG
docker tag winspector stefanscherer/winspector:linux

docker push stefanscherer/winspector-linux:linux-$TRAVIS_TAG
docker push stefanscherer/winspector-linux:linux
