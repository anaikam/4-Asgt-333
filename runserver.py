#!/usr/bin/env python
#-----------------------------------------------------------------------
# server.py
#
#-----------------------------------------------------------------------
import sys
import argparse
import courses
#-----------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(
        description="Server for the registrar application")

    parser.add_argument('port', nargs=1, type = int,
        help='the port at which the server should listen')

    parser.parse_args()
    # If statement to ensure we don't accept more than 1 argument.
    if len(sys.argv) != 2:
        print('Usage: python %s port' % sys.argv[0])
        sys.exit(2)
    try:
        port = int(sys.argv[1])
    except Exception:
        print('Port must be an integer.', file=sys.stderr)
        sys.exit(2)

    try:
        courses.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
