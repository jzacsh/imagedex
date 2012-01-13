Generate a JSON representation of a given directory listing, like so:

```bash
$ imagedex -P repo ./ | python -mjson.tool
```

```javascript
{
    "repo": [
        "./.gitignore", 
        "./imagedex.py", 
        "./readme.md", 
        {
            ".git": [
                "./.git/packed-refs", 
                "./.git/FETCH_HEAD", 
                "./.git/description", 
                "./.git/ORIG_HEAD", 
                "./.git/COMMIT_EDITMSG", 
                "./.git/HEAD", 
                "./.git/index", 
                "./.git/config"
            ]
        }, 
        {
            "imagedex": [
                "./imagedex/__init__.py", 
                "./imagedex/__init__.pyc"
            ]
        }
    ]
}
```

Almost everything about the output is configurable via command line options.

```bash
$ imagedex -j jsonPcallBack -P repo ./ | python -mjson.tool
```

```javascript
jsonPcallBack({
    "repo": [
        / * ... */
    ]
})
```

#Use:
  To see all available flags and options, run: ```imagedex.py -h```

  I run this script as a response to inotify events; only generating a .json file
  when something in the target directory supposedly changes.
  For a live example, see [`api_drawings`][apid] script I run on my web server:

```bash
while inotifywait --excludei='.*.swp' -r -e modify /some/dir/; do
    imagedex -r -j callBack -p '/api/3/' -f /api/path/imagedex.json /some/dir
done
```

##TODO:
* Write proper unit tests for all our little quirks

##Notes:
* Be aware that the `-r` recursive option is a lie and only provides data for a single directory level down.

[apid]: https://github.com/jzacsh/bin/blob/master/share/api_drawings#L20-28