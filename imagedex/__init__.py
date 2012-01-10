# -*- coding: utf-8 -*-
"""
  Imagedex

  Generate a JSON representation of a given directory listing.
"""

import os
import sys
from optparse import OptionParser
import simplejson as json
import io

#make code in this file a bit more readable
OSW_LABEL = 0
OSW_DIRS  = 1
OSW_FILES = 2

class _dotdict(dict):
    """Hackery to mimmic the dot notation of optpasre.parse_args()
    """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def config_defaults():
    """Imagedex default options
    """
    defaults = _dotdict()

    defaults.path = None
    defaults.outf = None
    defaults.recursive = False
    defaults.prefix = ''
    defaults.white = None
    defaults.var = 'imagedex'
    defaults.prop = 'files'
    defaults.native = False
    return defaults

def config():
    """Definition for acceptable options with python's optparse library.
    """
    defs = config_defaults()
    parser = OptionParser(usage='%prog [options] PATH')
    parser.add_option('-f', '--file', dest='outf',
        help="File you'd like your JSON index written to.")
    parser.add_option('-r', '--recursive', dest='recursive',
            action='store_true', default=defs.recursive,
        help="Recursively index any given directories in PATH.")
    parser.add_option('-p', '--prefix', dest='prefix', default=defs.prefix,
        help="Prefix you'd like to utilize for the file paths.")
    parser.add_option('-w', '--white', dest='white',
        help=("Whitelist of file extensions you'd like exclusively included,"
        ' comma-delimited.'))
    parser.add_option('-P', '--property', dest='prop', default=defs.prop,
        help=("Javascript property you'd like your array of data to live"
        ' inside of within the global JSON object.'))
    parser.add_option('-N', '--native', dest='native', action='store_true',
        default=defs.native, help='Output native python data, for instead of'
        ' converting to JSON. (Note: returned data structure is different,'
        ' depending on -r flag).')

    return parser

class Imagedex():
    def __init__(self, conf=None):
        """Initalize configuration if not already there
        """
        if conf:
            self.conf = conf
        else:
            self.conf = config_defaults()

    def index(self):
        """Return our final JSON string given our self.conf list has been
        properly initialized.
        """
        #digest our white list
        if self.conf.white:
            white = self.conf.white.lower().split(',')
        else:
            white = self.conf.white

        #get an actual index of requested path
        self.nativeindex = self.indexer()
        if self.nativeindex:
            if self.conf.native:
                index = self.nativeindex
            else:
                #wrap in some sort of proper javascript
                index = '{ "%s": ' % (self.conf.prop)

                #prepare a python-list of items to pass to json.dumps()
                self.items = []
                if self.conf.recursive:
                    #rebuild self.nativeindex using new structure, self.items,
                    # to be useful to json.dumps()
                    self.recurseJSON()

                else:
                    #dealing with only files is simple, structure is already
                    #useful to json.dumps()
                    self.renderJSONFiles(self.nativeindex)

                #let simplejson.dumps() do its thing
                index += json.dumps(self.items)

                #finish outter JSON wrapping.
                index += '}'
        else:
            #no data
            if self.conf.native:
                index = self.nativeindex
            else:
                index = '{ "%s": [] } ' % (self.conf.prop)

        return index

    def _prefix(self):
        """Generate a default prefix based on our base PATH
        """
        if not self.conf:
            return None
        elif self.conf.prefix:
            return self.conf.prefix
            #return None #real return
        return self.conf.path

    def indexer(self):
        """Return a listing of filesystem {path}, optionally only including files
        who's extension is in {white}.
        """

        passed = []

        # determine how much data we want, depending on recurisve option
        if self.conf.recursive:
            listing = os.walk(self.conf.path)
        else:
            listing = os.listdir(self.conf.path)

        # collect our data, regardless of depth, depending on our need for
        # white-listing.
        for name in listing:
            if self.conf.white:
                if name.split('.').pop() in white:
                    #this is a file with an extension we actually want.
                    passed.append(name)
            else:
                #we want files, regardless of extension
                passed.append(name)

        return passed

    def recurseJSON(self):
        """Map our native, python data structure of os.walk to, to something
        easily passed to json.dumps().

        os.walk produces a list of tuples as such:
            [('item#', "item's dirs", "item's files"), (...), ... ]

        we want a structure, in JSON, as such:
            lists of files, where files that are directories are tuples, with
            the first key as their directory-name, and the second key as their
            list of files (dirctory contents). eg.:
               [
                   #python list is our JSON array

                   'f1',

                   #python dictionary is our JSON object
                   {
                   'f2 (a dir)': [
                       #everything in this list is identical in concept to the
                       # very outter list.
                       'file1',
                       'file2',
                       {
                       'sub3 dir': [
                           'boop', 'doop'
                           ]
                       }
                       ]
                   },

                   'f3'
               ]
        """
        index = ''

        depth = len(self.nativeindex[0][OSW_DIRS])
        self.rendering = 0
        #@TODO: recurse, down directory listings
        while (self.rendering <= depth):
            listing = self.nativeindex[self.rendering]
            self.renderJSONFiles(listing[OSW_FILES])
            self.renderJSONDirs()
            self.rendering += 1
            break #@TODO: remove this if you ever write true recursion

        return index

    def renderJSONFiles(self, files):
        """render files, according to the JSON format we publish"""
        for item in files:
            self.items.append(self._prefix() + item)

    def renderJSONDirs(self):
        """render directories, according to the JSON format we publish

        @note: for the purposes of this project's actual deployment, real
        recursion wasn't needed. only a single level is traversed.
        """
        for item in self.nativeindex[self.rendering][OSW_DIRS]:
            subDir = { item : [] }

            #find the directory listing in our tuple, that represents 'item'
            for dirset in self.nativeindex:
                if os.path.basename(dirset[0]) == item:
                    for subFile in dirset[OSW_FILES]:
                        subDir[item].append(self._prefix() + item + '/' + subFile)
                    self.items.append(subDir)

# vim: et:ts=4:sw=4:sts=4
