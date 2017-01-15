#!/bin/bash
set -e

docker tag winspector stefanscherer/winspector:linux-$TRAVIS_TAG

docker push stefanscherer/winspector:linux-$TRAVIS_TAG

set +e
echo "Waiting for Windows image stefanscherer/winspector:windows-$TRAVIS_TAG"
until docker run --rm winspector stefanscherer/winspector:windows-$TRAVIS_TAG
do
  sleep 15
  echo "Try again"
done
set -e

echo "Downloading manifest-tool"
wget https://github.com/luxas/manifest-tool/releases/download/v0.3.0/manifest-tool
chmod +x manifest-tool
./manifest-tool

echo "Pushing manifest stefanscherer/winspector:$TRAVIS_TAG"
./manifest-tool push from-args \
  --platforms linux/amd64,windows/amd64 \
  --template stefanscherer/winspector:ARCH-$TRAVIS_TAG \
  --target stefanscherer/winspector:$TRAVIS_TAG

echo "Pushing manifest stefanscherer/winspector:latest"
./manifest-tool push from-args \
  --platforms linux/amd64,windows/amd64 \
  --template stefanscherer/winspector:ARCH-$TRAVIS_TAG \
  --target stefanscherer/winspector:latest
