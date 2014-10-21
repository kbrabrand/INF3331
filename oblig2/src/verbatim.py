import re;

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()