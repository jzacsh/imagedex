#!/usr/bin/env node

var fs = require('fs');
var util = require('util');

var dirs = [
  './public/',
//'./public/paper/',
//'./public/tablet/',
]

var index = {};

var parseDir = function(dir) {
  console.log('... parsing directory: %s\n', dir);
  fs.readdir(dir, function(err, files) {
    if (err) {
      console.log('error parsing dir..: %s\n', util.inspect(err)); //@TODO: remove me!!    
      return 1;
    }

    parseFiles(dir, files);
  });
}

var parseFiles = function(path, f) {
  for (var file in f) {
    console.log('... parsing file: %s\n', f[file]); //@TODO: remove me!!    

    var fullPath = path + f[file];

    if (isDir(fullPath)) {
      console.log(); //@TODO: remove me!!    
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

console.log('...starting'); //@TODO: remove me!!    

process.argv.forEach(function(val, index, array) {
  console.log('val[%s]: %s\n', index, val);
});

for (var d in dirs) {
  parseDir(dirs[d]);
}
console.log('...done'); //@TODO: remove me!!    
