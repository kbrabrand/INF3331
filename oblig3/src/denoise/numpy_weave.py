import numpy as np;      # NumPy
import copy;             # Tool for copying objects/arrays
from PIL import Image;   # Python image library
from scipy import weave; # Weave. For C, you know..

import shared;                            # Shared logic for denoise
from weave_c import support_c, denoise_c; # Import denoising algorithm and support stuff

def denoise_image_data(data0, width, height, kappa=1.0, iterations=1, manipulations={}):
    # Get number of channels per pixel
    channels = 1;

    # If shape has more than two list items, the list is three dimensional
    # and we'll get the number of values per list in the 2nd dimension
    if len(data0.shape) > 2:
        channels = data0.shape[2];

    # Make copy of the image data
    data1 = copy.deepcopy(data0);

    man_r = manipulations['lr'];
    man_g = manipulations['lg'];
    man_b = manipulations['lb'];
    man_h = manipulations['lh'];
    man_s = manipulations['ls'];
    man_i = manipulations['li'];

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
            'man_r',
            'man_g',
            'man_b',
            'man_h',
            'man_s',
            'man_i'
        ],
        force = 1,
        support_code = support_c
    );

    return data1;

def denoise_file(source, destination, kappa=1.0, iterations=1, manipulations={}):
    # Load image data from input file into an numpy.ndarray
    try:
        data = np.array(Image.open(source))
    except IOError:
        print 'Source file [%s] could not be loaded.' % source;
        exit();

    # Get width and height based on the data shape
    height, width = data.shape[:2];

    # Perform denoising of image
    denoised_data = denoise_image_data(data, width, height, kappa, iterations, manipulations);

    # Ouput denoised image data to new file
    try:
        Image.fromarray(denoised_data).save(destination);
    except IOError:
        print 'Destination file [%s] was not writeable.' % destination;
        exit();