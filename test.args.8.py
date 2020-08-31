#!/usr/bin/env python
import sys
import argparse
# https://stackoverflow.com/questions/27681718/using-python-argparse-on-repeating-groups
def parse_args():

    # Create the first parser object and get just the first parameter
    parser = argparse.ArgumentParser('Argument format parser')
    parser.add_argument('arg_format', type=str, help='The first argument.' +
                        'It tells us what input to expect next.')
    args_ns, remaining = parser.parse_known_args()

    # Generate a new parser based on the first parameter
    parser = formatSpecificParser(args_ns.arg_format)

    # There will always be at least one set of input (in this case at least)
    args_ns, remaining = parser.parse_known_args(args=remaining, namespace=args_ns)

    # Iterate over the remaining input, if any, adding to the namespace
    while remaining:
        args_ns, remaining = parser.parse_known_args(args=remaining,
                                                     namespace=args_ns)

    return args_ns

def formatSpecificParser(arg_format):
    parser = argparse.ArgumentParser("Command line parser for %s" % arg_format)
    if (arg_format == "format_1"):
        addArgsFormat1(parser)
    # elif (...):
        # other format function calls
    return parser

def addArgsFormat1(parser):
    parser.add_argument('arg1', type=str, action='append', help='helpful text')
    parser.add_argument('arg2', type=str, action='append', help='helpful text')
    parser.add_argument('arg3', type=str, action='append', help='helpful text')

def main(argv):
    args = parse_args()
    print (args)

if __name__ == "__main__":
    main(sys.argv[1:])