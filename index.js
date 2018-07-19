#!/usr/bin/env node
'use strict';

const async = require('async');
const request = require('request');

const username = process.env.DOCKER_USER || 'username';
const password = process.env.DOCKER_PASS || 'password';

const commandLineArgs = require('command-line-args');

const optionDefinitions = [
  { name: 'verbose', alias: 'v', type: Boolean },
  { name: 'src', alias: 's', type: String, defaultOption: true },
  { name: 'help', alias: 'h', type: Boolean }
];

const options = commandLineArgs(optionDefinitions);

const showUsage = () => {
  console.log('Usage: winspector image');
  process.exit(1);
};

const parseImageArg = imagename => {
  let found = imagename.match(/^([^.\/:]+)\/([^:]+):(.*)$/);
  if (found) {
    return { reg: 'registry-1.docker.io', path: `${found[1]}/${found[2]}`, org: found[1], image: found[2], tag: found[3] };
  }
  found = imagename.match(/^([^\/:]+)\/([^:]+):(.*)$/);
  if (found) {
    return { reg: found[1], path: found[2], org: '', image: found[2], tag: found[3] };
  }
  found = imagename.match(/^([^.\/:]+)\/([^:]+)$/);
  if (found) {
    return { reg: 'registry-1.docker.io', path: `${found[1]}/${found[2]}`, org: found[1], image: found[2], tag: 'latest' };
  }
  found = imagename.match(/^([^\/:]+)\/([^:]+)$/);
  if (found) {
    return { reg: found[1], path: found[2], org: '', image: found[2], tag: 'latest' };
  }
  found = imagename.match(/^([^.\/:]+):(.*)$/);
  if (found) {
    return { reg: 'registry-1.docker.io', path: `${found[1]}/${found[2]}`, org: 'library', image: found[1], tag: found[2] };
  }
  return { reg: 'registry-1.docker.io', path: `${found[1]}/${found[2]}`, org: 'library', image: imagename, tag: 'latest' };
};

const parseArgs = () => {
  if (options.help) {
    showUsage();
  }

  if (!options.src) {
    console.log('Error: src image missing.');
    showUsage();
  }

  options.images = {};
  options.images.src = parseImageArg(options.src);

  if (options.verbose) {
    console.log(options);
  }
};

parseArgs();

let bearer;
let manifestSource;
let configSource;
let manifestSourceBase;
let configSourceBase;
let manifestTargetBase;
let configTargetBase;
let manifestTarget;
let configTarget;
let upload;

const knownWindowsLayers = require('./knownWindowsLayers.json');

const getTokenForSourceImage = callback => {
  request(
    `https://auth.docker.io/token?account=${username}&scope=repository%3A${options.images.src.org}%2F${options.images.src.image}%3Apull&service=registry.docker.io`,
    {
      json: true,
      auth: {
        username,
        password,
        sendImmediately: false
      }
    },
    (err, res, body) => {
      if (err) {
        return callback(err);
      }
      bearer = body.token;
      callback(null);
    }
  );
};

const getManifestOfSourceImage = callback => {
  console.log(
    `Retrieving information about source image ${options.images.src.path}:${options.images.src.tag}`
  );
  request(
    {
      url: `https://${options.images.src.reg}/v2/${options.images.src.path}/manifests/${options.images.src.tag}`,
      auth: {
        bearer
      },
      json: true,
      headers: {
        Accept: 'application/vnd.docker.distribution.manifest.v2+json, application/vnd.docker.distribution.manifest.list.v2+json'
      }
    },
    (err, res, body) => {
      if (err) {
        return callback(err);
      }
      if (
        body.mediaType ===
        'application/vnd.docker.distribution.manifest.list.v2+json'
      ) {
        options.images.src.tag = body.manifests[0].digest;
        getManifestOfSourceImage(() => {
          if (options.verbose) {
            console.log('source manifest:', manifestSource);
          }
          return callback(null);
        });
      } else {
        manifestSource = body;
        if (options.verbose) {
          console.log('source manifest:', manifestSource);
        }
        callback(null);
      }
    }
  );
};

const getConfigOfSourceImage = callback => {
  request(
    {
      url: `https://${options.images.src.reg}/v2/${options.images.src.org}/${options.images.src.image}/blobs/${manifestSource.config.digest}`,
      auth: {
        bearer
      },
      json: true
    },
    (err, res, body) => {
      if (err) {
        return callback(err);
      }
      if (options.verbose) {
        console.log(
          'src image os:',
          body.os,
          'os.version:',
          body['os.version']
        );
        console.log('src image diff_ids:', body.rootfs.diff_ids);
      }
      configSource = body;
      callback(null);
    }
  );
};

const inspectSourceImage = callback => {
  console.log(
    `Image name: ${options.images.src.org}/${options.images.src.image}`
  );
  console.log('Tag:', options.images.src.tag);
  console.log('Number of layers:', manifestSource.layers.length);

  console.log('Schema version:', manifestSource.schemaVersion);
  console.log('Architecture:', configSource.architecture);
  console.log(
    `Created: ${configSource.created} with Docker ${configSource.docker_version} on ${configSource.os} ${configSource['os.version']}`
  );
  var totalSize = 0;
  var appSize = 0;
  console.log('Sizes of layers:');
  manifestSource.layers.forEach(layer => {
    console.log(`  ${layer.digest} - ${layer.size} byte`);
    totalSize += layer.size;
    if (
      layer.mediaType !==
      'application/vnd.docker.image.rootfs.foreign.diff.tar.gzip'
    ) {
      appSize += layer.size;
    }
  });
  console.log(`Total size (including Windows base layers): ${totalSize} byte`);
  console.log(`Application size (w/o Windows base layers): ${appSize} byte`);
  console.log('Windows base image used:');
  if (configSource.os !== 'windows') {
    console.log('  It does not seem to be a Windows image');
  }
  manifestSource.layers.forEach(layer => {
    if (
      layer.mediaType ==
      'application/vnd.docker.image.rootfs.foreign.diff.tar.gzip'
    ) {
      const known = knownWindowsLayers[layer.digest];
      if (known) {
        console.log(`  ${known}`);
      } else {
        console.log(`  ${layer.digest} - unknown Windows layer`);
      }
    }
  });

  console.log('History:');
  configSource.history.forEach(hist => {
    if (hist.created_by.substr('#(nop)') !== -1) {
      let cmd = hist.created_by;
      cmd = cmd.replace(/.*#\(nop\)\s*/, '');
      console.log('  ', cmd);
    } else {
      console.log('  RUN', hist.created_by);
    }
  });
};

async.series(
  [
    getTokenForSourceImage,
    getManifestOfSourceImage,
    getConfigOfSourceImage,

    inspectSourceImage,

    callback => {
      console.log('Done.');
    }
  ],
  errSeries => {
    if (errSeries) {
      console.log('Error:', errSeries);
    }
  }
);
