import re;
import os.path;
import verbatim;

def get_regex_match_in_file(file, regex):
    """
    Open the given file and return what ever the regex match in the file.

    Parameters
    ----------
    file : str
        Path to the file to search for something in.
    regex : str
        Regex to match for in the file.

    Returns
    -------
    file_content : str
        Augmented file content

    Example
    -------
    Match patterin in this file (valid file + content that exist)
    >>> get_regex_match_in_file('./code_import.py', '(def get_regex(.*))+')
    'def get_regex_match_in_file(file, regex):'

    Match pattern in non-existant file
    >>> get_regex_match_in_file('./non-existant-file', 'foobar')
    Traceback (most recent call last):
    ...
    Exception: Failed reading file [./non-existant-file]

    Match pattern that will never be present, in file that exist
    >>> get_regex_match_in_file('./code_import.py', '($a)')
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

def inject_source_code(file_content, pretty=False, base_path=''):
    r"""
    Replace all "%@ import..." statements in the latex file with the source code
    it refers to.

    Parameters
    ----------
    file_content : str
        The file_content to search for and replace placeholders in.
    pretty : bool
        Whether or not to use fancy formatting.
    base_path : str
        Base path that the input paths are relative to

    Returns
    -------
    file_content : str
        Augmented file content

    Example
    -------
    Test that the input string is returned when there's no match
    >>> inject_source_code('a few words')
    'a few words'

    Test that a valid import statement is parsed and injected
    >>> inject_source_code('foobar\n%@import ./code_import.py (def get_regex(.*))+\nstuff')
    'foobar\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nstuff'

    Test that a string containing two import statements is handled correctly
    >>> inject_source_code('foobar\n%@import ./code_import.py (def get_regex(.*))+\nstuff\n%@import ./code_import.py (def get_regex(.*))+\nmore stuff')
    'foobar\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nstuff\n\\begin{verbatim}\ndef get_regex_match_in_file(file, regex):\\end{verbatim}\n\nmore stuff'
    """

    # Find all lines matching the import statement format
    source_imports = re.findall(r'\n(%@import ([^\ ]+) (.*))\n', file_content);

    # For each import statement
    for source_import in source_imports:
        import_statement = source_import[0];
        import_regex     = source_import[2];

        file_path = source_import[1];
        file_base = os.path.split(file_path)[0];

        if base_path != '':
            file_path = os.path.join(base_path, file_path);
            file_base = os.path.split(file_path)[0];

        # Replace import statement with the matched portion
        # of the referenced file
        file_content = file_content.replace(
            import_statement,
            verbatim.verbatim_code(
                get_regex_match_in_file(file_path, import_regex),
                pretty
            )
        );

    return file_content;

if __name__ == "__main__":
    import doctest
    doctest.testmod()