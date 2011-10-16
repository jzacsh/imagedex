#TODO:
* Abstract as necessary to turn this into a python module as well as its current CLI utility.
* Write ability to manage options via ConfigParser config file.
* Write super-simle python/js web response (eg.: slideshow) in examples/, and use wsgi in the process

#Purpose:
  Keep a JSON index of your images and only re-index what's needed, when
  needed, on inotify's queue.

##Use:
  I intend to run this script as a response to inotify events; only generating
  a .json file when something in the target has supposedly changed.

