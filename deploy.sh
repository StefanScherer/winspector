#!/bin/bash
set -e

docker tag winspector stefanscherer/winspector:linux-$TRAVIS_TAG

docker push stefanscherer/winspector:linux-$TRAVIS_TAG

set +e
echo "Waiting for Windows image stefanscherer/winspector:windows-$TRAVIS_TAG-2016"
until docker run --rm winspector stefanscherer/winspector:windows-$TRAVIS_TAG-2016
do
  sleep 15
  echo "Try again"
done
echo "Waiting for Windows image stefanscherer/winspector:windows-$TRAVIS_TAG-1709"
until docker run --rm winspector stefanscherer/winspector:windows-$TRAVIS_TAG-1709
do
  sleep 15
  echo "Try again"
done
set -e

echo "Downloading docker client with manifest command"
wget https://6582-88013053-gh.circle-artifacts.com/1/work/build/docker-linux-amd64
mv docker-linux-amd64 docker
chmod +x docker
./docker version

set -x

echo "Pushing manifest $image:$TRAVIS_TAG"
./docker manifest create "$image:$TRAVIS_TAG" \
  "$image:linux-$TRAVIS_TAG" \
  "$image:windows-$TRAVIS_TAG-2016" \
  "$image:windows-$TRAVIS_TAG-1709"
./docker manifest push "$image:$TRAVIS_TAG"

echo "Pushing manifest $image:latest"
./docker manifest create "$image:latest" \
  "$image:linux-$TRAVIS_TAG" \
  "$image:windows-$TRAVIS_TAG-2016" \
  "$image:windows-$TRAVIS_TAG-1709"
./docker manifest push "$image:latest"
