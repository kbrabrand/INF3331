#!/usr/bin/env python

import sys        # interpreter tools
import re         # Regular expression tools
import subprocess # Subprocess module
import shlex      # Simple lexical analysis

def add_pretty_print_block(file_content):
    """
Add instructions for setting up pretty printing of source code and execution
results after the documentclass instruction.

file_content : str
    The file_content to add the instructions to."""

    pretty_print_setup = ("\usepackage{fancyvrb}\n"
                          "\usepackage{framed}\n"
                          "\usepackage{color}\n"
                          "\providecommand{\shadedwbar}{}\n"
                          "\definecolor{shadecolor}{rgb}{0.87843, 0.95686, 1.0}\n"
                          "\\renewenvironment{shadedwbar}{\n"
                          "\def\FrameCommand{\color[rgb]{0.7,     0.95686, 1}\\vrule width 1mm\\normalcolor\colorbox{shadecolor}}\FrameRule0.6pt\n"
                          "\MakeFramed {\\advance\hsize-2mm\FrameRestore}\\vskip3mm}{\\vskip0mm\endMakeFramed}\n"
                          "\providecommand{\shadedquoteBlueBar}{}\n"
                          "\\renewenvironment{shadedquoteBlueBar}[1][]{\n"
                          "\\bgroup\\rmfamily\n"
                          "\\fboxsep=0mm\\relax\n"
                          "\\begin{shadedwbar}\n"
                          "\list{}{\parsep=-2mm\parskip=0mm\\topsep=0pt\leftmargin=2mm\n"
                          "\\rightmargin=2\leftmargin\leftmargin=4pt\\relax}\n"
                          "\item\\relax}\n"
                          "{\endlist\end{shadedwbar}\egroup}\n");

    match = re.search(r'(\\documentclass{.*})', file_content);

    if (match):
        return file_content.replace(
            match.group(0),
            match.group(0) + "\n" + pretty_print_setup
        );
    else:
        raise Exception('No documentclass found');

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

def inject_source_code(file_content, pretty=False):
    """
Replace all "%@ import..." statements in the latex file with the source code
it refers to.

Parameters
----------
file_content : str
    The file_content to search for and replace placeholders in.
pretty : bool
    Whether or not to use fancy formatting or not.
    """

    # Find all lines matching the import statement format
    source_imports = re.findall(r'\n(%@import ([^\ ]+) (.*))\n', file_content);

    if (pretty):
        before = ("\\begin{shadedquoteBlueBar}\n"
                  "\\fontsize{9pt}{9pt}\n"
                  "\\begin{Verbatim}\n");

        after  = ("\\end{Verbatim}\n"
                  "\\end{shadedquoteBlueBar}\n"
                  "\\noindent\n");
    else:
        before = '\\begin{verbatim}\n';
        after  = '\end{verbatim}\n';

    # For each import statement
    for source_import in source_imports:
        import_statement = source_import[0];
        import_file      = source_import[1];
        import_regex     = source_import[2];

        # Replace import statement with the matched portion
        # of the referenced file
        file_content = file_content.replace(
            import_statement,
            before +
            get_regex_match_in_file(import_file, import_regex) + '\n' +
            after
        );

    return file_content

def inject_script_output(file_content, pretty=False):
    """
Replace all "%@ exec..." statements in the latex file with the source code
it refers to.

Parameters
----------
file_content : str
    The file_content to search for and replace placeholders in.
pretty : bool
    Whether or not to use fancy formatting or not.
    """

    if (pretty):
        before = '\\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},labelposition=topline,framesep=2.5mm,framerule=0.7pt]\n';

        after  = ("\\end{Verbatim}\n"
                  "\\noindent\n");
    else:
        before = '\\begin{verbatim}\n';
        after  = '\end{verbatim}\n';

    # Find all lines matching the exec statement format
    script_execs = re.findall(r'\n(%@exec (.*))\n', file_content);

    # For each exec statement
    for script_exec in script_execs:
        exec_statement = script_exec[0];
        exec_script    = script_exec[1];

        # Replace each statement with the script output in a verbatim block
        file_content = file_content.replace(
            exec_statement,
            before + '$ ' + exec_script + '\n' +
            get_exec_result(exec_script) +
            after
        );

    return file_content

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
    """

    file_content = open(input).read();

    if (pretty):
        # Inject latex pretty print stuff before preamble
        file_content = add_pretty_print_block(file_content);

    # Replace "%@ import..." statements with matched line in source file
    file_content = inject_source_code(file_content, pretty);

    # Replace "%@ exec..." statements with output from script execution
    file_content = inject_script_output(file_content, pretty);

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
    pretty      = True if (l >= 4) else False;
    verbose     = False;

    process_file(input_file, output_file, verbose, pretty);

