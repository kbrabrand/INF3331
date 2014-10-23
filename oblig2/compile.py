#!/usr/bin/env python

import subprocess;
import argparse;
import re;

def compile_latex_file(source, destination, interactive, verbose=False):
    """
Return code wrapped in verbatim block.

source : str
    Path to latex source file
destination : str
    Path to where the compiled file should be put
interactive : str
    Whether to enable interaction with latex compiler or not"""

    arguments = ['pdflatex', '-file-line-error'];

    # Set interaction to nonstopmode if interactive is not set to
    # a truthive value
    if interactive == False:
        if verbose:
            print '* enabling nonstopmode';

        arguments.append('-interaction=nonstopmode');

    # Add output destination directory if provided
    if destination != False:
        if verbose:
            print '* setting output directory to: ' % destination;

        arguments.append('-output-directory');
        arguments.append(destination);

    # Append source file to argument array
    arguments.append(source);

    if verbose:
        print '* starting subprocess: ' + ' '.join(arguments) + '\n\n';

    proc = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE
    );

    out, err = proc.communicate()

    error_lines = re.findall(r'.*:[0-9]+:.*', out);

    if len(error_lines) > 0:
        print "\n".join(error_lines) + "\n";

    print "\n".join(out.splitlines()[-2:]);

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compile PDF from latex file.');

    parser.add_argument('--interactive', '-i', dest='interactive', help="Interact with the latex compiler", action='store_true');

    parser.add_argument('source',  metavar='S', help='Latex source file');

    parser.add_argument('--destination', '-d', metavar='D',
                        dest='destination', help='Path to where the compiled file should be put',
                        default=False);

    parser.add_argument('--verbose', '-v', dest='verbose', help="Enable verbose script output", action='store_true');

    args = parser.parse_args();

    compile_latex_file(
        args.source,
        args.destination,
        args.interactive,
        args.verbose
    );