import re         # Regular expression tools
import subprocess # Subprocess module
import ntpath;    # Path extraction tools

import verbatim;
import code_import;
import script_execution;
import inline_blocks;
import latex;

def process_content(file_content, verbose=False, pretty=False, base_path=''):
    """
    Process latex document content and augument it with source code,
    execution results and other logic on top of plain old latex.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    verbose : bool
        Be loud about what to do.
    pretty : bool
        Use fancy formatting for code blocks and output.
    base_path : str
        Base path that the input paths are relative to

    Returns
    -------
    file_content : str
        Augmented file content"""

    # Insert content of files referenced by \input instruction
    file_content = latex.process_input_instructions(file_content, verbose, pretty, base_path);

    # Replace "%@import..." statements with matched line in source file
    file_content = code_import.inject_source_code(file_content, pretty, base_path);

    ## Replace "%@exec..." statements with output from script execution
    file_content = script_execution.inject_script_output(file_content, pretty);

    ## Replace inline source code statement; "%@(import|exec) .... %@"
    file_content = inline_blocks.process_blocks(file_content, pretty);

    ## Replace fake code/exec statements
    file_content = inline_blocks.process_fake(file_content, pretty);

    return file_content;

def process_file(input, output, verbose=False, pretty=False):
    """
    Loads an input file, runs it through the processor and
    outputs the result to the output file.

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
    >>> process_file('./non-existant-input-file', 'test')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./non-existant-input-file]

    Test that an exception is thrown when writing fails (in this case
    by writing to a folder that does not exist)
    >>> process_file('../tests/doctest-fixtures/tex_before.tex', '../tmp/abc/test.tex')
    Traceback (most recent call last):
    ...
    Exception: Failed writing file [../tmp/abc/test.tex]

    Test that successfull pre-processing of latex file gives no output
    >>> process_file('../tests/doctest-fixtures/tex_before.tex', '../tmp/test.tex')
    """

    try:
        file_content = open(input).read();
    except IOError as e:
        raise Exception('Failed reading file [' + input + ']');

    # Extract head part of path. We'll use it later when loading files
    # relative to the file we're preprocessing
    base_path, tail = ntpath.split(input)

    if (pretty):
        # Inject latex pretty print stuff before preamble
        file_content = latex.add_pretty_print_block(file_content);

    # Process content
    file_content = process_content(file_content, verbose, pretty, base_path);

    # Write to output file
    try:
        output_file = open(output, 'w');
        output_file.write(file_content);
        output_file.close();
    except IOError as e:
        raise Exception('Failed writing file [' + output + ']');

if __name__ == "__main__":
    import doctest
    doctest.testmod()