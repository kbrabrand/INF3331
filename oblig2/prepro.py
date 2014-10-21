#!/usr/bin/env python

import re         # Regular expression tools
import subprocess # Subprocess module
import argparse;  # Argument parsing tools

from src import verbatim;
from src import code_import;
from src import script_execution;
from src import inline_blocks;
from src import latex;

def process_file(input, output, verbose=False, pretty=False):
    """
    Process a latex file and augment it with source code, execution results and
    logic on top of plain old latex.

    Parameters
    ----------
    input : str
        Path to the input file to process.
    output : str
        Where to store the processed (and enriched) file.
    verbose : bool
        Be loud about what to do.
    pretty : bool
        Use fancy formatting for code blocks and output.

    Test that exception is given if reading of input file fails
    >>> process_file('./none-existant-input-file', 'test')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./none-existant-input-file]

    Test that an exception is thrown when writing fails (in this case
    by writing to a folder that does not exist)
    >>> process_file('./tests/doctest-fixtures/tex_before.tex', './tmp/abc/test.tex')
    Traceback (most recent call last):
    ...
    Exception: Failed writing file [./tmp/abc/test.tex]

    Test that successfull pre-processing of latex file gives no output
    >>> process_file('./tests/doctest-fixtures/tex_before.tex', './tmp/test.tex')
    """

    try:
        file_content = open(input).read();
    except IOError as e:
        raise Exception('Failed reading file [' + input + ']');

    # Insert content of files referenced by \input instruction
    file_content = latex.process_input_instructions(file_content);

    if (pretty):
        # Inject latex pretty print stuff before preamble
        file_content = latex.add_pretty_print_block(file_content);

    # Replace "%@import..." statements with matched line in source file
    file_content = code_import.inject_source_code(file_content, pretty);

    # Replace "%@exec..." statements with output from script execution
    file_content = script_execution.inject_script_output(file_content, pretty);

    # Replace inline source code statement; "%@(import|exec) .... %@"
    file_content = inline_blocks.process_blocks(file_content, pretty);

    # Replace fake code/exec statements
    file_content = inline_blocks.process_fake(file_content, pretty);

    # Write to output file
    try:
        output_file = open(output, 'w');
        output_file.write(file_content);
        output_file.close();
    except IOError as e:
        raise Exception('Failed writing file [' + output + ']');


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

    process_file(
        args.source,
        args.destination,
        args.verbose,
        args.pretty
    );