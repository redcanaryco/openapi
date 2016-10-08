import logging
import code
import sys
import redcanary


def main(args=sys.argv[1:]):
    from optparse import OptionParser

    parser = OptionParser("usage: scavenger [options] <input file>...")

    parser.add_option("-v", "--verbose", dest="verbose",
                      help="Be chatty",
                      action="store_true", default=False)

    (opts, args) = parser.parse_args(args)
    logging.root.setLevel(logging.DEBUG if opts.verbose else logging.INFO)

    rc = redcanary.RedCanaryClient()
    code.interact(banner="Welcome to the Red Canary API. Your API client is in the `rc` variable",
                  local=locals())


if __name__ == '__main__':
    exit(main())
