#!/usr/bin/env node

var fs = require('fs');
var util = require('util');

var index = {};

var isDir = function (path) {
  var directory = new Boolean(false);
  fs.stat(path, function(err, stat) {
    if (!err) {
      console.log('isDir().. `stat` object:\n\t%s\n',
        util.inspect(stat.isDirectory()));
      directory = stat.isDirectory();
    }
  });
  return directory;
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

var dirs = (function () {
  if (process.argv.length > 2) {
    return process.argv.slice(2);
  }
  else {
    return [
      './public/paper/',
      './public/tablet/'
    ];
  }
})();


var parseDir = function(dir) {
  console.log('... parsing directory: %s\n', dir);
  fs.readdir(dir, function(err, files) {
    if (err) {
      console.log('error parsing dir..: %s\n', util.inspect(err));
    }

    parseFiles(dir, files);
  });
}

var parseFiles = function(path, f) {
  for (var file in f) {
    console.log('... parsing file: %s\n', f[file]); //@TODO: remove me!!    

    var fullPath = path + f[file];

    if (isDir(fullPath)) {
      console.log('...found directory, recursing:\n\t%s', fullPath); //@TODO: remove me!!    
      parseDir(fullPath);
    }
    else {
      fs.stat(fullPath, function(err, stats) {
        if (err) {
          console.log('error: %s\n', err); //@TODO: remove me!!    
          return 1;
        }
        else {
          console.log('stats: %s\n', util.inspect(stats)); //@TODO: remove me!!    
          if (!(path in index)) {
            index[path] = [];
          }
          index[path].push({
            name: f[file],
            type: fileType(f[file]),
            size: stats.size
          });
        }
      });
    }
  }
}

console.log('...starting'); //@TODO: remove me!!    

for (var d in dirs) {
  parseDir(dirs[d]);
}
