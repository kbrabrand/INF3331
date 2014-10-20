#!/usr/bin/env python

import re         # Regular expression tools
import subprocess # Subprocess module
import shlex      # Simple lexical analysis
import argparse;  # Argument parsing tools

verbatim_plain_pre =   '\\begin{verbatim}'
verbatim_plain_post =  '\end{verbatim}\n'

verbatim_code_pretty_pre =  ("\\begin{shadedquoteBlueBar}\n"
                             "\\fontsize{9pt}{9pt}\n"
                             "\\begin{Verbatim}\n");

verbatim_code_pretty_post = ("\\end{Verbatim}\n"
                             "\\end{shadedquoteBlueBar}\n"
                             "\\noindent\n");

verbatim_exec_pretty_pre =  "\\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},labelposition=topline,framesep=2.5mm,framerule=0.7pt]"

verbatim_exec_pretty_post = ("\\end{Verbatim}\n"
                             "\\noindent\n");

def verbatim_code(code, pretty=False):
    r"""
    Return code wrapped in verbatim block.

    code : str
        String of code to wrap in verbatim.
    pretty : bool
        Whether to use fancy formatting or not.

    Test plain verbatim print
    >>> verbatim_code("foobar")
    '\\begin{verbatim}\nfoobar\\end{verbatim}\n'

    Test fancy verbatim code print
    >>> verbatim_code("foobar", pretty=True)
    '\\begin{shadedquoteBlueBar}\n\\fontsize{9pt}{9pt}\n\\begin{Verbatim}\n\nfoobar\\end{Verbatim}\n\\end{shadedquoteBlueBar}\n\\noindent\n'
    """

    if (pretty):
        before = verbatim_code_pretty_pre;
        after  = verbatim_code_pretty_post;
    else:
        before = verbatim_plain_pre;
        after  = verbatim_plain_post;

    return before + '\n' + code + after;

def verbatim_exec(result, pretty=False):
    r"""
    Return execution result wrapped in verbatim block.

    result : str
        String with output from execution to wrap in verbatim.
    pretty : bool
        Whether to use fancy formatting or not.

    Test plain verbatim print
    >>> verbatim_exec("foobar")
    '\\begin{verbatim}\nfoobar\\end{verbatim}\n'

    Test fancy verbatim exec result print
    >>> verbatim_exec("foobar", pretty=True)
    '\\begin{Verbatim}[numbers=none,frame=lines,label=\\fbox{{\\tiny Terminal}},fontsize=\\fontsize{9pt}{9pt},labelposition=topline,framesep=2.5mm,framerule=0.7pt]\nfoobar\\end{Verbatim}\n\\noindent\n'
    """

    if (pretty):
        before = verbatim_exec_pretty_pre
        after  = verbatim_exec_pretty_post;
    else:
        before = verbatim_plain_pre;
        after  = verbatim_plain_post;

    return before + '\n' + result + after;

def add_pretty_print_block(file_content):
    r"""
    Add instructions for setting up pretty printing of source code and execution
    results after the documentclass instruction.

    file_content : str
        The file_content to add the instructions to.

    Test adding pretty print instructions to document missing documentclass
    >>> add_pretty_print_block('1337 bits of rubbish');
    Traceback (most recent call last):
    ...
    Exception: No documentclass found

    Test adding pretty print instructions to document with documentclass
    >>> add_pretty_print_block('\\documentclass{article}\nstuff')
    '\\documentclass{article}\n\\usepackage{fancyvrb}\n\\usepackage{framed}\n\\usepackage{color}\n\\providecommand{\\shadedwbar}{}\n\\definecolor{shadecolor}{rgb}{0.87843, 0.95686, 1.0}\n\\renewenvironment{shadedwbar}{\n\\def\\FrameCommand{\\color[rgb]{0.7,     0.95686, 1}\\vrule width 1mm\\normalcolor\\colorbox{shadecolor}}\\FrameRule0.6pt\n\\MakeFramed {\\advance\\hsize-2mm\\FrameRestore}\\vskip3mm}{\\vskip0mm\\endMakeFramed}\n\\providecommand{\\shadedquoteBlueBar}{}\n\\renewenvironment{shadedquoteBlueBar}[1][]{\n\\bgroup\\rmfamily\n\\fboxsep=0mm\\relax\n\\begin{shadedwbar}\n\\list{}{\\parsep=-2mm\\parskip=0mm\\topsep=0pt\\leftmargin=2mm\n\\rightmargin=2\\leftmargin\\leftmargin=4pt\\relax}\n\\item\\relax}\n{\\endlist\\end{shadedwbar}\\egroup}\n\nstuff'
    """

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

    Match patterin in this file (valid file + content that exist)
    >>> get_regex_match_in_file('./prepro.py', '(def get_regex(.*))+')
    'def get_regex_match_in_file(file, regex):'

    Match pattern in non-existant file
    >>> get_regex_match_in_file('./non-existant-file', 'foobar')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./non-existant-file]

    Match pattern that will never be present, in file that exist
    >>> get_regex_match_in_file('./prepro.py', '($a)')
    ''
    """

    try:
        file_content = open(file).read();
    except IOError as e:
        raise Exception('Failed reading file [' + file + ']');

    match = re.findall(r'' + regex, file_content);

    # If something matched, return the first group of the first match.
    # Otherwise, return an empty string.
    if (len(match) == 0):
        return '';
    else:
        return match[0][0];

def get_exec_result(command):
    """
    Parse and execute a command and return the result.

    Parameters
    ----------
    command : str
        Command to execute.

    Test valid command, echoing a number
    >>> get_exec_result('echo 1337')
    '1337\\n'

    Test invalid command, and expect Exception
    >>> get_exec_result('\o\ |o| /o/')
    Traceback (most recent call last):
    ...
    Exception: Execution of command failed
    """

    # Parse/split the command into arguments
    arguments = shlex.split(command);

    try:
        # Open a sub process with the arguments
        process   = subprocess.Popen(arguments, stdout=subprocess.PIPE);

        # Get the piped output and return
        out, err = process.communicate();
    except OSError as e:
        raise Exception('Execution of command failed');

    return out;

def inject_source_code(file_content, pretty=False):
    r"""
    Replace all "%@ import..." statements in the latex file with the source code
    it refers to.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether or not to use fancy formatting.

    Test that the input string is returned when there's no match
    >>> inject_source_code('a few words')
    'a few words'

    Test that a valid import statement is parsed and injected
    >>> inject_source_code('foobar\n%@import ./prepro.py (def get_regex(.*))+\nstuff')
    'foobar\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nstuff'

    Test that a string containing two import statements is handled correctly
    >>> inject_source_code('foobar\n%@import ./prepro.py (def get_regex(.*))+\nstuff\n%@import ./prepro.py (def get_regex(.*))+\nmore stuff')
    'foobar\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nstuff\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nmore stuff'
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
            verbatim_code(
                get_regex_match_in_file(import_file, import_regex),
                pretty
            )
        );

    return file_content

def inject_script_output(file_content, pretty=False):
    r"""
    Replace all "%@exec..." statements in the latex file with the source code
    it refers to.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether or not to use fancy formatting.

    Test that an exec statement is matched and converted to a verbatim block
    >>> inject_script_output('foobar\n%@exec echo 1337\n')
    'foobar\n\\begin{verbatim}\n$ echo 1337\n1337\n\\end{verbatim}\n\n'
    """

    if (pretty):
        before = verbatim_exec_pretty_pre;
        after  = verbatim_exec_pretty_post;
    else:
        before = verbatim_plain_pre;
        after  = verbatim_plain_post;

    # Find all lines matching the exec statement format
    script_execs = re.findall(r'\n(%@exec (.*))\n', file_content);

    # For each exec statement
    for script_exec in script_execs:
        exec_statement = script_exec[0];
        exec_script    = script_exec[1];

        # Replace each statement with the script output in a verbatim block
        file_content = file_content.replace(
            exec_statement,
            verbatim_exec(
                '$ ' + exec_script + '\n' + get_exec_result(exec_script),
                pretty
            )
        );

    return file_content

def process_inline_blocks(file_content, pretty=False):
    r"""
    Identify all inline code and exec result blocks and format them in the same
    fashion as the exec result blocks pulled from referenced files.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether to use fancy formatting or not

    Test that code import blocks are picked up and formatted
    >>> process_inline_blocks('foobar\n%@import\n<?php\nvar_dump($_POST);\n%@\ntest\n%@import\ndef test(a, b):\n    print \'foobar\';\n%@\nstuff')
    "foobar\n\\begin{verbatim}\n<?php\nvar_dump($_POST);\n\\end{verbatim}\n\ntest\n\\begin{verbatim}\ndef test(a, b):\n    print 'foobar';\n\\end{verbatim}\n\nstuff"

    Test that exec result blocks are picked up and formatted
    >>> process_inline_blocks('foobar\n%@exec\n$ echo "Just another Perl hacker"\n%@\nstuff')
    'foobar\n\\begin{verbatim}\n$ echo "Just another Perl hacker"\n\\end{verbatim}\n\nstuff'
    """

    # Find all lines matching the exec or import statement format
    blocks = re.findall(r'(%@(import|exec)\n((.*\n)+?)%@)', file_content, re.MULTILINE);

    # For each import statement
    for block in blocks:
        outer_block = block[0];
        block_type  = block[1];
        inner_block = block[2];

        if (inner_block == "import"):
            formatted_block = verbatim_code(inner_block, pretty);
        else:
            formatted_block = verbatim_exec(inner_block, pretty);

        file_content = file_content.replace(
            outer_block,
            formatted_block
        );

    return file_content;

def process_inline_fake(file_content, pretty=False):
    r"""
    Identify inline code blocks to execute, execute it and print the code blocks.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether to use fancy formatting or not

    >>> process_inline_fake('foobar\n%@bash fakescript.sh\necho 1337\n%@\nstuff\n%@python fakepython.py\nprint 1337\n%@\nmore stuff')
    'foobar\n\\begin{verbatim}\n$ bash fakescript.sh \n1337\n\\end{verbatim}\n\nstuff\n\\begin{verbatim}\n$ python fakepython.py \n1337\n\\end{verbatim}\n\nmore stuff'
    """

    # Find inline code blocks for execution
    blocks = re.findall(r'(%@(bash|python) (.*)\n((.*\n)+?)%@)', file_content, re.MULTILINE);

    for block in blocks:
        code_type    = block[1]; # python or bash
        fake_command = block[2];
        code_block   = block[3];

        # Open a sub process for executing the code block
        process   = subprocess.Popen([code_type, '-c', code_block], stdout=subprocess.PIPE);

        # Get the piped output and return
        out, err = process.communicate();

        # Replace each statement with the script output in a verbatim block
        file_content = file_content.replace(
            block[0],
            verbatim_exec(
                '$ %s %s \n%s' % (code_type, fake_command, out),
                pretty
            )
        );

    return file_content;

def process_input_instructions(file_content):
    r"""
    Identify latex input instructions and replace them with the actual instructions
    from the referenced files.

    Parameters
    ----------
    file_content : str
        The file_content to add the instructions to.

    Test that exception is thrown when a non-existant file is provided for input
    >>> process_input_instructions('foo\n\input{./non-existant-file}\nmore stuff')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./non-existant-file]

    Test that a valid file referenced with an input statement is injected
    >>> process_input_instructions('foo\n\input{./tests/doctest-fixtures/abc.tex}\nstuff');
    'foo\nhei\nstuff'
    """

    input_instructions = re.findall(r'(\\input{(.*)})', file_content);

    for input_instruction in input_instructions:
        file_name = input_instruction[1];

        try:
            input_content = open(file_name).read();
        except IOError as e:
            raise Exception('Failed reading file [' + file_name + ']');

        file_content = file_content.replace(input_instruction[0], input_content);

    return file_content;

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

    # Insert content of files referenced by \input instruction
    file_content = process_input_instructions(file_content);

    if (pretty):
        # Inject latex pretty print stuff before preamble
        file_content = add_pretty_print_block(file_content);

    # Replace "%@import..." statements with matched line in source file
    file_content = inject_source_code(file_content, pretty);

    # Replace "%@exec..." statements with output from script execution
    file_content = inject_script_output(file_content, pretty);

    # Replace inline source code statement; "%@(import|exec) .... %@"
    file_content = process_inline_blocks(file_content, pretty);

    # Replace fake code/exec statements
    file_content = process_inline_fake(file_content, pretty);

    # Write to output file
    output_file = open(output, 'w');
    output_file.write(file_content);
    output_file.close();


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