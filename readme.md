#TODO:
* Utilize optparse to allow for flags indicating an output file
* Write js front-end app (eg.: slideshow) in examples/

#Purpose:
  Keep a JSON index of your images and only re-index what's needed, when
  needed, on inotify's queue.

##Use:
  I intend to run this script as a response to inotify events; only generating
  a .json file when something in the target has supposedly changed.

