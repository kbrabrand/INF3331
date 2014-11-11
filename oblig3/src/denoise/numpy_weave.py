import numpy as np;      # NumPy
import copy;             # Tool for copying objects/arrays
from PIL import Image;   # Python image library
from scipy import weave; # Weave. For C, you know..

from weave_c import support_c, denoise_c; # Import denoising algorithm and support stuff

def denoise_image_data(data0, width, height, kappa=1.0, iterations=1, manipulations={}):
    """
    Performs denoising and/or manipulation of image data.

    Parameters
    ----------
    data0 : numpy_array
        Array containing the image information. 2-dim for monochrome
        images and 3-dim for color images.
    width : int
        Image width in pixels.
    height : int
        Image height in pixels.
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
    numpy_array
        NumpPy array with the same shape as the data0 parameter containing
        manipulated image data.
    """

    # Get number of channels per pixel
    channels = 1;

    # If shape has more than two list items, the list is three dimensional
    # and we'll get the number of values per list in the 2nd dimension
    if len(data0.shape) > 2:
        channels = data0.shape[2];

    # Make copy of the image data
    data1 = copy.deepcopy(data0);

    man_r = manipulations['lr'] if 'lr' in manipulations.keys() else 0;
    man_g = manipulations['lg'] if 'lg' in manipulations.keys() else 0;
    man_b = manipulations['lb'] if 'lb' in manipulations.keys() else 0;
    man_h = manipulations['lh'] if 'lh' in manipulations.keys() else 0;
    man_s = manipulations['ls'] if 'ls' in manipulations.keys() else 0;
    man_i = manipulations['li'] if 'li' in manipulations.keys() else 0;

    weave.inline(
        denoise_c,
        [
            'data0',
            'data1',
            'width',
            'height',
            'channels',
            'kappa',
            'iterations',
            'man_r', # Manipulation of R component
            'man_g', # Manipulation of G component
            'man_b', # Manipulation of B component
            'man_h', # Manipulation of H component
            'man_s', # Manipulation of S component
            'man_i'  # Manipulation of I component
        ],
        support_code = support_c
    );

    return data1;

def denoise_file(source, destination, kappa=1.0, iterations=1, manipulations={}):
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

    Empty string is returned upon successful denoising
    >>> denoise_file('../../assets/disasterbefore.jpg', '../../tmp/out.jpg')
    """

    # Load image data from input file into an numpy.ndarray
    try:
        data = np.array(Image.open(source))
    except IOError:
        return 'Source file [%s] could not be loaded.' % source;

    # Get width and height based on the data shape
    height, width = data.shape[:2];

    # Perform denoising of image
    denoised_data = denoise_image_data(data, width, height, kappa, iterations, manipulations);

    # Ouput denoised image data to new file
    try:
        Image.fromarray(denoised_data).save(destination);
    except IOError:
        return 'Destination file [%s] was not writeable.' % destination;

if __name__ == "__main__":
    import doctest;
    doctest.testmod();