#!/usr/bin/env python2

"""
  Imagedex

  Command-line utility wrapping imagedex methods.
"""

import os
import io
import sys
import imagedex as imagedex

def config():
    """Manage command-line considerations for given optparsing that's been
    setup by the imagedex code itself.
    """

    parser = imagedex.config()
    (opts, args) = parser.parse_args()

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

    opts.path = args[0]
    return opts

def cli():
    opts = config() #wrapper to config, specific to cli
    imaged = imagedex.Imagedex(opts)

    #call the necessary functions in Imagedex class to produce actual index
    index = imaged.index()

    #finally output data as JSON
    if opts.outf:
        f = io.FileIO(opts.outf, 'w')
        f.write(index)
        f.close()
    else:
        print index

if __name__ == '__main__':
  cli()

# vim: et:ts=4:sw=4:sts=4
