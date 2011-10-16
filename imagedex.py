#!/usr/bin/env python2.6

import os
import sys
import simplejson as json

def usage():
  usage = """
  Usage: %s PATH
    Generate JSON representation of the given directory, PATH.
  """ % (sys.argv[0])
  sys.stderr.write('%s\n' % usage)

def main():
  if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
    usage()
    sys.exit(1)

  #get an actual index of requested path
  index = os.listdir(sys.argv[1]) #test data

  #finally output data as JSON
  print json.dumps(index)

if __name__ == '__main__':
  main()
