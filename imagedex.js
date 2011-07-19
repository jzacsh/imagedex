#!/usr/bin/env node

var fs = require('fs');
var util = require('util');

var dirs = [
  './public/img/paper/',
  './public/img/tablet/',
]

var index = {};

var parseDir = function(dir) {
  fs.readdir(dir, function(err, files) {
    if (err) {
      console.debug('error parsing dir..: %s\n', err);
      return 1;
    }

    parseFiles(dir, files);
  });
}

var parseFiles = function(path, files) {
  for (var f in files) {
    console.log('file: %s\n\tobject: %s\n\tfs.stat(): %s\n',
      files[f], util.inspect(files[f], true), util.inspect(fs.Stats(files[f]).isDirectory()));

    var fullPath = dir + files[f];

    if (isDir(fullPath)) {
      parseDir(fullPath);
    }
    else {
      fs.stats(fullPath, function(err, stats) {
        if (err) {
          console.debug('error: %s\n', err);
          return 1;
        }
        else {
          console.log('stats: %s\n', stats);
          index[dir].push({
            name: files[f],
            type: fileType(files[f]),
            size: stats.size
          });
        }
      });
    }
  }
}

for (var d in dirs) {
  parseDir(dirs[d]);
}

var isDir = function (path) {
  fs.stat(path, function(err, stat) {
    if (!err) {
      console.log('isDir().. `stat` object:\n\t%s\n',
        util.inspect(stat.isDirectory()));
      return stat.isDirectory();
    }
  });
}

var fileType = function (p) {
  var dot = p.substring((p.length - 4), (p.length - 3));
  if (dot === '.') {
    return p.substring((p.length - 3))
      .toLowerCase();
  }
  else {
    return null;
  }
}
