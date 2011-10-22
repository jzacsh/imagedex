#TODO:
* Default to a prefix (-p) of whatever PATH argument was, regardless of passing -p.
* Write proper unit tests for all our little quirks.
* Write ability to manage options via ConfigParser config file.
* Write a super-simple javascript slideshow based on JSON data

#Purpose:
  Generate a JSON representation of a given directory listing.

##Use:
  I intend to run this script as a response to inotify events; only generating
  a .json file when something in the target has supposedly changed.

