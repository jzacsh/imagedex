#TODO:
* Write proper unit tests for all our little quirks.

#Purpose:
  Generate a JSON representation of a given directory listing.

##Use:
  I run this script as a response to inotify events; only generating a .json file
  when something in the target directory supposedly changes.
  For a live example, see [`api_drawings`][apid] script I run on my web server:

```bash
while inotifywait --excludei='.*.swp' -r -e modify "/some/dir/"; do
    imagedex -j callBack -p '/api/3/' -r -f /api/path/imagedex.json /some/dir
done
```
  
[apid]: https://github.com/jzacsh/bin/blob/master/share/api_drawings#L20-28