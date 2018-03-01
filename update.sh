#!/bin/bash

docker=~/bin/docker

images="microsoft/windowsservercore microsoft/nanoserver microsoft/windowsservercore:1709 microsoft/nanoserver:1709 microsoft/windowsservercore-insider microsoft/nanoserver-insider"
cat knownWindowsLayers.json | jq . > work.json

for image in $images; do 
  osversion=$($docker manifest inspect -v $image 2>/dev/null | jq -r '.Platform["os.version"]')
  sha=$($docker manifest inspect -v $image 2>/dev/null | jq -r '.SchemaV2Manifest.layers[].digest' | tail -1)
  img=${image%:*}
  echo "$sha -> $img:$osversion"
  val=$img:$osversion
  cat work.json | jq ". + { \"$sha\": \"$val\" }" >work$$.json
  cp work$$.json work.json
done

mv work.json knownWindowsLayers.json
