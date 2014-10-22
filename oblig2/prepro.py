#!/usr/bin/env python

import argparse;
from src import prepro;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Compile PDF from latex file.');

    parser.add_argument('source',  metavar='source', help='Path to preprocess source file');

    parser.add_argument('destination', metavar='dest',
                        help='Destination folder for the processed file');

    parser.add_argument('--pretty', '-p', dest='pretty', help="Enable fancy verbatims",
                        action='store_true', default=True);

    parser.add_argument('--verbose', '-v', dest='verbose',
                        help="Enable verbose script output", action='store_true');

    args = parser.parse_args();

    prepro.process_file(
        args.source,
        args.destination,
        args.verbose,
        args.pretty
    );