#!/usr/bin/env python

import subprocess
import sys;
import re;

def compile_latex_file(path_to_file):
    """
Return code wrapped in verbatim block.

path_to_file : str
    Path to latex file to process"""

    proc = subprocess.Popen(
        "pdflatex -file-line-error -interaction=nonstopmode %s" % path_to_file,
        shell=True,
        stdout=subprocess.PIPE
    );

    out, err = proc.communicate()

    error_lines = re.findall(r'.*:[0-9]+:.*', out);

    print "\n".join(error_lines) + "\n";
    print "\n".join(out.splitlines()[-2:]);

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    l = len(sys.argv)

    if l < 2:
        print "Not enough arguments included."
        print "usage: %s input_file " % sys.argv[0];
        sys.exit(0);

    input_file  = sys.argv[1];

    compile_latex_file(input_file);