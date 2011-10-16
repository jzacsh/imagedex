#TODO:
* Write proper unit tests for all our little quirks.
* Abstract imagedex/__init__.py as necessary to make sure it only returns methods, like a proper python module
* Pull CLI-only code from imagedex/__init__.py into imagedex/imagedex.py
* Write ability to manage options via ConfigParser config file.
* Write super-simle python/js web response (eg.: slideshow) in examples/, and use wsgi in the process

#Purpose:
  Generate a JSON representation of a given directory listing.

##Use:
  I intend to run this script as a response to inotify events; only generating
  a .json file when something in the target has supposedly changed.

