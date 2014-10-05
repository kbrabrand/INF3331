#!/usr/bin/env python

import sys        # interpreter tools
import re         # Regular expression tools
import subprocess # Subprocess module
import shlex      # Simple lexical analysis

def get_regex_match_in_file(file, regex):
    """
Open the given file and return what ever the regex match in the file.

Parameters
----------
file : str
    Path to the file to search for something in.
regex : str
    Regex to match for in the file.
    """

    match = re.findall(r'' + regex, open(file).read());

    # If something matched, return the first group of the first match.
    # Otherwise, return an empty string.
    if (len(match) == 0):
        return '';
    else:
        return match[0][0];

def get_exec_result(command):
    """
Execute the command and return the result.

Parameters
----------
command : str
    Command to execute.
    """

    # Parse/split the command into arguments
    arguments = shlex.split(command);

    # Open a sub process with the arguments
    process   = subprocess.Popen(arguments, stdout=subprocess.PIPE);

    # Get the piped output and return
    out, err = process.communicate();

    return out;

def inject_source_code(file_content):
    """
Replace all "%@ import..." statements in the latex file with the source code
it refers to.

Parameters
----------
file_content : str
    The file_content to search for and replace placeholders in.
    """

    # Find all lines matching the import statement format
    source_imports = re.findall(r'\n(%@import ([^\ ]+) (.*))\n', file_content);

    # For each import statement
    for source_import in source_imports:
        import_statement = source_import[0];
        import_file      = source_import[1];
        import_regex     = source_import[2];

        # Replace import statement with the matched portion
        # of the referenced file
        file_content = file_content.replace(
            import_statement,
            '\\begin{verbatim}\n' +
            get_regex_match_in_file(import_file, import_regex) + '\n' +
            '\end{verbatim}\n'
        );

    return file_content

def inject_script_output(file_content):
    """
Replace all "%@ exec..." statements in the latex file with the source code
it refers to.

Parameters
----------
file_content : str
    The file_content to search for and replace placeholders in.
    """

    # Find all lines matching the exec statement format
    script_execs = re.findall(r'\n(%@exec (.*))\n', file_content);

    # For each exec statement
    for script_exec in script_execs:
        exec_statement = script_exec[0];
        exec_script    = script_exec[1];

        # Replace each statement with the script output in a verbatim block
        file_content = file_content.replace(
            exec_statement,
            '\\begin{verbatim}\n' +
            '$ ' + exec_script + '\n' +
            get_exec_result(exec_script) +
            '\end{verbatim}\n'
        );

    return file_content

def process_file(input, output, verbose=False):
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
    """

    file_content = open(input).read();

    # Replace "%@ import..." statements with matched line in source file
    file_content = inject_source_code(file_content);

    # Replace "%@ exec..." statements with output from script execution
    file_content = inject_script_output(file_content);

    # Write to output file
    output_file = open(output, 'w');
    output_file.write(file_content);
    output_file.close();


# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    l = len(sys.argv)

    if l < 3:
        print "Not enough arguments included."
        print "usage: %s input output " % sys.argv[0];
        sys.exit(0)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    process_file(input_file, output_file);

