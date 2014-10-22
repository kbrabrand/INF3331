import re;
import os.path;

def add_pretty_print_block(file_content):
    r"""
    Add instructions for setting up pretty printing of source code and execution
    results after the documentclass instruction.

    Parameters
    ----------
    file_content : str
        The file_content to add the instructions to.

    Returns
    -------
    file_content : str
        Augmented file content

    Example
    -------
    Test adding pretty print instructions to document missing documentclass
    >>> add_pretty_print_block('1337 bits of rubbish');
    Traceback (most recent call last):
    ...
    Exception: No documentclass found

    Test adding pretty print instructions to document with documentclass
    >>> add_pretty_print_block('\\documentclass{article}\nstuff')
    '\\documentclass{article}\n\\usepackage{fancyvrb}\n\\usepackage{framed}\n\\usepackage{color}\n\\providecommand{\\shadedwbar}{}\n\\definecolor{shadecolor}{rgb}{0.87843, 0.95686, 1.0}\n\\renewenvironment{shadedwbar}{\n\\def\\FrameCommand{\\color[rgb]{0.7,     0.95686, 1}\\vrule width 1mm\\normalcolor\\colorbox{shadecolor}}\\FrameRule0.6pt\n\\MakeFramed {\\advance\\hsize-2mm\\FrameRestore}\\vskip3mm}{\\vskip0mm\\endMakeFramed}\n\\providecommand{\\shadedquoteBlueBar}{}\n\\renewenvironment{shadedquoteBlueBar}[1][]{\n\\bgroup\\rmfamily\n\\fboxsep=0mm\\relax\n\\begin{shadedwbar}\n\\list{}{\\parsep=-2mm\\parskip=0mm\\topsep=0pt\\leftmargin=2mm\n\\rightmargin=2\\leftmargin\\leftmargin=4pt\\relax}\n\\item\\relax}\n{\\endlist\\end{shadedwbar}\\egroup}\n\nstuff'
    """

    pretty_print_setup =    ("\usepackage{fancyvrb}\n"
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

def process_input_instructions(file_content, base_path=''):
    r"""
    Identify latex input instructions and replace them with the actual instructions
    from the referenced files.

    Parameters
    ----------
    file_content : str
        The file_content to add the instructions to.
    base_path : str
        Base path that the input paths are relative to

    Returns
    -------
    file_content : str
        Augmented file content

    Example
    -------
    Test that exception is thrown when a non-existant file is provided for input
    >>> process_input_instructions('foo\n\input{./non-existant-file}\nmore stuff')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./non-existant-file]

    Test that a valid file referenced with an input statement is injected
    >>> process_input_instructions('foo\n\input{../tests/doctest-fixtures/abc.tex}\nstuff');
    'foo\nhei\n\n1337\n\nstuff'
    """

    input_instructions = re.findall(r'(\\input{(.*)})', file_content);

    for input_instruction in input_instructions:
        file_path = input_instruction[1];
        file_base = os.path.split(file_path)[0];

        if base_path != '':
            file_path = os.path.join(base_path, file_path);
            file_base = os.path.split(file_path)[0];

        try:
            input_content = process_input_instructions(
                open(file_path).read(),
                file_base
            );
        except IOError as e:
            raise Exception('Failed reading file [' + file_path + ']');

        file_content = file_content.replace(input_instruction[0], input_content);

    return file_content;

if __name__ == "__main__":
    import doctest
    doctest.testmod()