#!/usr/bin/env node

var fs = require('fs');
var util = require('util');

var index = {};

var isDir = function (path) {
  var directory = 0;
  fs.statSync(path, function(err, stat) {
    if (!err) {
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
      './public/'
    ];
  }
})();


var parseDir = function(dir) {
  console.log('... parsing directory: %s\n', dir);
  fs.readdirSync(dir, function(err, files) {
    if (err) {
      console.log('error parsing dir..: %s\n', util.inspect(err));
    }

    parseFiles(dir, files);
  });
}

var parseFiles = function(path, f) {
  for (var file in f) {
    console.log('... parsing something in "%s": %s\n', path, f[file]); //@TODO: remove me!!    

    var fullPath = path + f[file];

    if (isDir(fullPath)) {
      console.log('...DIRECTORY, recursing:\n\t%s', fullPath); //@TODO: remove me!!    
      parseDir(fullPath);
    }
    else {
      //@TODO: problem, using ASYNC functions, this callback is run when the
      //data for _this_ scope is already on the last item (eg.: "tablet")...
      //consider using [...]Sync() versions of all these `fs` functions.

      fs.statSync(fullPath, function(err, stats) {
        if (err) {
          console.log('error: %s\n', err); //@TODO: remove me!!    
          return 1;
        }
        else {
          if (!(path in index)) {
            index[path] = [];
          }
          index[path].push({
            name: f[file],
            type: fileType(f[file]),
            size: stats.size
          });
          console.log('... FILE:\n\tnamed: "%s"\n\tstats: %s\n\n\tfs: %s\n',
            index[path][index[path].length - 1].name,
            util.inspect(index[path][index[path].length - 1]),
            util.inspect(stats)); //@TODO: remove me!!    
        }
      });
    }
  }
}

console.log('STARTING...'); //@TODO: remove me!!    

for (var d in dirs) {
  parseDir(dirs[d]);
}
