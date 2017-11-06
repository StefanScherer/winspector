[![This image on DockerHub](https://img.shields.io/docker/pulls/stefanscherer/winspector.svg)](https://hub.docker.com/r/stefanscherer/winspector/) [![Build status](https://ci.appveyor.com/api/projects/status/9nw1nk799cqtmdw2/branch/master?svg=true)](https://ci.appveyor.com/project/StefanScherer/winspector/branch/master) [![Build Status](https://travis-ci.org/StefanScherer/winspector.svg?branch=master)](https://travis-ci.org/StefanScherer/winspector)

# Winspector - a Windows Docker Image Inspector

A little utility to fetch info on a particular Windows Docker image from the public Docker registry. See also the blog post https://stefanscherer.github.io/winspector/

Derived work from https://github.com/giantswarm/inspect-docker-image, thanks Giant Swarm!

## Running the CLI

A public Docker image `stefanscherer/winspector` is available for Linux and Windows Docker engines. Docker will download the right version for you automatically.

Execute, to fetch info on `golang:1.8-nanoserver`, for example:

```
docker run --rm stefanscherer/winspector golang:1.8-nanoserver
```

See below for example output.

## Development

Set up your Node.js environment for development like this:

```nohighlight
git clone https://github.com/StefanScherer/winspector.git
cd winspector/
npm install
```

You can then execute the CLI like this:

```nohighlight
node index.js golang:1.8-nanoserver
```

## CLI example output

The output looks something like this:

```nohighlight
Image name: library/golang
Tag: 1.8-nanoserver
Number of layers: 10
Sizes of layers:
  sha256:5496abde368a3dd39999745bf998c877ddc6a390a943bc3fd99ffaabf728ed88 - 242646586 byte
  sha256:482ab31872a23b32cbdeca13edb7a0b97290714c0b5edcce96fbb3e34221ea91 - 100529622 byte
  sha256:66c4c0000446f244c31261d2b9981fcba14207a8a48ab548fc937eeb7e898899 - 952 byte
  sha256:fadb3cd88a6267200344acf26b376f4eb2bbe1e27a468e0439cdfabd52856aba - 955 byte
  sha256:6ad305fc60a3da44f0d081e690f57a4dd19f978de968be84957950b1bcbcaa92 - 855435 byte
  sha256:70ec80188525acbc38d74063e1c40e38214e07aa73340723948378cb5319a819 - 968 byte
  sha256:fd1bc4c4fdccb66cdd96bb199187e34cc204ad8de57168895e49d8df2efb13ba - 955 byte
  sha256:fdedc809027b75bd2570c7c8a7c631f1c6151026ea00d7eb33e4598c8d2652d3 - 952 byte
  sha256:574c52669c35b13f6cc4937eb42016b745cd2c459d52eb59c1f03b87ebfc218c - 96531566 byte
  sha256:b465e25782dc6ebef9d1c15e233332a46698a3de4e4fb0bcfd99da624ceeacfd - 961 byte
Total size (including Windows base layers): 440568952 byte
Application size (w/o Windows base layers): 97392744 byte
Windows base image used:
  microsoft/nanoserver:10.0.14393.206 base
  microsoft/nanoserver:10.0.14393.447 update
```
