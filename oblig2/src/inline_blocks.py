import subprocess;
import re;
import verbatim;

def process_blocks(file_content, pretty=False):
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
    >>> process_blocks('foobar\n%@import\n<?php\nvar_dump($_POST);\n%@\ntest\n%@import\ndef test(a, b):\n    print \'foobar\';\n%@\nstuff')
    "foobar\n\\begin{verbatim}\n<?php\nvar_dump($_POST);\n\\end{verbatim}\n\ntest\n\\begin{verbatim}\ndef test(a, b):\n    print 'foobar';\n\\end{verbatim}\n\nstuff"

    Test that exec result blocks are picked up and formatted
    >>> process_blocks('foobar\n%@exec\n$ echo "Just another Perl hacker"\n%@\nstuff')
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
            formatted_block = verbatim.verbatim_code(inner_block, pretty);
        else:
            formatted_block = verbatim.verbatim_exec(inner_block, pretty);

        file_content = file_content.replace(
            outer_block,
            formatted_block
        );

    return file_content;

def process_fake(file_content, pretty=False):
    r"""
    Identify inline code blocks to execute, execute it and print the code blocks.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether to use fancy formatting or not

    >>> process_fake('foobar\n%@bash fakescript.sh\necho 1337\n%@\nstuff\n%@python fakepython.py\nprint 1337\n%@\nmore stuff')
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
            verbatim.verbatim_exec(
                '$ %s %s \n%s' % (code_type, fake_command, out),
                pretty
            )
        );

    return file_content;

if __name__ == "__main__":
    import doctest
    doctest.testmod()