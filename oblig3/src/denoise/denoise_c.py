import subprocess;   # Subprocess module
import numpy as np;  # Numpy
import Image;        # Image tools
from os import path; # Path helpers

from shared import should_do_manipulation;

def denoise_file(source, destination, kappa, iterations, manipulations={}):
    """
    Ferforms denoising of the source file and outputs the response to the
    destination file.

    Parameters
    ----------
    source: str
        Path to the file to denoise.
    destination : str
        Path to the destination (output) file.
    kappa : float
        The denoising factor. Allowed range: [0.0-1.0]
    iterations : int
        Number of interations to do with the denoising.
    manipulations : dict
        Specification of the manipulations to do. Expected keys: lr (R component
        in RGB), lg (G component in RGB), lb (B component in RGB), lh (H component
        in HSI), ls (S component in HSI) and li (I component in HSI).

    Returns
    -------
    output : str
        Empty string if OK. Error output if something didn't go right.

    Example
    -------
    Error message returned if source does not exist
    >>> denoise_file('non-existant.jpg', 'foo.jpg', 0.1, 10)
    'Source file [non-existant.jpg] could not be loaded.'

    Error message returned if color image is provided
    >>> denoise_file('../../assets/disasterbeforecolor.jpg', 'foobar.jpg', 0.1, 10);
    'Color images are not supported in C backend.'

    Error message returned if manipulations are requested
    >>> denoise_file('../../assets/disasterbefore.jpg', 'foobar.jpg', 0.1, 10, {'lr': 100});
    'Manipulations are not supported i C backend'

    Empty string is returned upon successful denoising
    >>> denoise_file('../../assets/disasterbefore.jpg', '../../tmp/out.jpg', 0.1, 10)
    ''
    """

    try:
        data = np.array(Image.open(source))
    except IOError:
        return 'Source file [%s] could not be loaded.' % source;

    # Get width and height based on the data shape
    if len(data.shape) > 2:
        return 'Color images are not supported in C backend.';

    # Give warning if manipulation is requested
    if should_do_manipulation(manipulations):
        return 'Manipulations are not supported i C backend';

    script_path = path.join(
        path.dirname(__file__),
        '../../lib/denoise'
    );

    # Parse/split the command into arguments
    arguments = arguments = [
        script_path,
        "%f" % kappa,
        "%d" % iterations,
        source,
        destination
    ];

    try:
        # Open a sub process with the arguments
        process   = subprocess.Popen(arguments, stdout=subprocess.PIPE);

        # Get the piped output and return
        out, err = process.communicate();
    except OSError as e:
        raise Exception('Execution of command failed');

    return out;

if __name__ == "__main__":
    import doctest;
    doctest.testmod();