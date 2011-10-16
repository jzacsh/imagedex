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

def indexer(path, white):
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

    #@TODO: write section to override options from Config parser!! perhaps -c
    # flag?
    (opts, args) = parser.parse_args()
    return (opts, args, parser)

def main():
    (opts, args, parser) = config()

    #sanity check
    if (len(args) != 1 or
    not os.path.isdir(args[0]) or
    not os.access(args[0], os.R_OK)):
        err = 'You must pass a readable directory, PATH, to be indexed.'
        parser.error(err)
        sys.exit(1)

    #more sanity check
    if (opts.outf and os.path.isfile(opts.outf)
        and not os.access(opts.outf, os.W_OK)):
        err = """File "{0}" already exists and is not writeable.\n""".format(
            opts.outf)
        sys.stderr.write(err)
        sys.exit(2)

    #digest our white list
    if opts.white:
        white = opts.white.lower().split(',')
    else:
        white = opts.white

    #get an actual index of requested path
    origindex = indexer(args[0], white)
    if origindex:
        #wrap in some sort of proper javascript
        index = 'var %s = { %s: ' % (opts.var, opts.prop)
        index += json.dumps([ opts.prefix + path for path in origindex ])
        index += '};'
    else:
        index = ''

    #finally output data as JSON
    if opts.outf:
        f = io.FileIO(opts.outf, 'w')
        f.write(index)
        f.close()
    else:
        print index

# vim: et:ts=4:sw=4:sts=4
