import subprocess; # Subprocess module
import shlex;      # Simple lexical analysis
import re;         # Regex tools

import verbatim;

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

    # Find all lines matching the exec statement format
    script_execs = re.findall(r'\n(%@exec (.*))\n', file_content);

    # For each exec statement
    for script_exec in script_execs:
        exec_statement = script_exec[0];
        exec_script    = script_exec[1];

        # Replace each statement with the script output in a verbatim block
        file_content = file_content.replace(
            exec_statement,
            verbatim.verbatim_exec(
                '$ ' + exec_script + '\n' + get_exec_result(exec_script),
                pretty
            )
        );

    return file_content;

if __name__ == "__main__":
    import doctest
    doctest.testmod()