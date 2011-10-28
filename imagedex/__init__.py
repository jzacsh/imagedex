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

def config():
    parser = OptionParser(usage='%prog [options] PATH')
    parser.add_option('-f', '--file', dest='outf',
        help="File you'd like your JSON index written to.")
    parser.add_option('-p', '--prefix', dest='prefix', default='',
        help="Prefix you'd like to utilize for the file paths.")
    parser.add_option('-w', '--white', dest='white',
        help=("Whitelist of file extensions you'd like exclusively included,"
        ' comma-delimited.'))
    parser.add_option('-n', '--var', dest='var', default='imagedex',
        help=("Javascript variable you'd like the JSON assigned to for proper"
        ' namespacin'))
    parser.add_option('-P', '--property', dest='prop', default='files',
        help=("Javascript property you'd like your array of data to live"
        ' inside of within the global JSON object.'))
    parser.add_option('-N', '--native', dest='native', action="store_true",
        default=False, help='Output native python data, for instead of '
        'converting to JSON.')

    #@TODO: return a list of both critical CLI and ConfigPars data
    # - return critical CLI-data (eg.: parser object) 
    # - return critical ConfigParser data
    # This should allow any caller utilize the tools returned
    dots = {} #@TODO: make this real ^

    return (dots, parser)

class Imagedex():
    def __init__(self, conf=None):
        """Initalize configuration if not already there
        """
        if conf:
            self.conf = conf
        else:
            #initialize conf from config files, ourself
            (dots, parser) = config()

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
        origindex = self.indexer(self.conf.path, white)
        if origindex:
            if self.conf.native:
                index = origindex
            else:
                #wrap in some sort of proper javascript
                index = 'var %s = { %s: ' % (self.conf.var, self.conf.prop)
                index += json.dumps([ self._prefix() + path for path in origindex ])
                index += '};'
        else:
            index = ''

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

    def indexer(self, path, white):
        """Return a listing of filesystem {path}, optionally only including files
        who's extension is in {white}.
        """

        listing = os.listdir(path)

        if white:
            approved = []
            for name in listing:
                if name.split('.').pop() in white:
                    approved.append(name)
            return approved
        else:
            return listing


# vim: et:ts=4:sw=4:sts=4
