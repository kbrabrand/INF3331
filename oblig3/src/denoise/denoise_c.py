import subprocess;   # Subprocess module
import numpy as np;  # Numpy
import Image;        # Image tools
from os import path; # Path helpers

from src.denoise.shared import should_do_manipulation;

def denoise_file(source, destination, kappa, iterations, manipulations={}):
    try:
        data = np.array(Image.open(source))
    except IOError:
        print 'Source file [%s] could not be loaded.' % source;
        exit();

    # Get width and height based on the data shape
    if len(data.shape) > 2:
        print 'Color images are not supported in C backend.';
        exit();

    # Give warning if manipulation is requested
    if should_do_manipulation(manipulations):
        print 'Manipulations are not supported i C backend';
        exit();

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