import numpy as np;      # NumPy
import copy;             # Tool for copying objects/arrays
from PIL import Image;   # Python image library
from scipy import weave; # Weave. For C, you know..

from src.denoise import shared; # Shared logic for denoise

def denoise_image_data(data0, width, height, kappa=1.0, iterations=1):
    code = """
    int i, j, iteration;

    // Temporary value variable
    float tmp;

    // Variables to store index positions in
    int current, one_up, one_right, one_down, one_left;

    // Pointers to use when performing the denoising
    npy_ubyte *source, *target;

    // Set the source and target pointers
    source = data0;
    target = data1;

    for (iteration=0; iteration<iterations; iteration++) {
        // On the first, third,... iteration, use data0 as source and
        // data 1 as target. On the second, fourth and so on, do it the
        // other way around.

        source = iteration%2 ? data1 : data0;
        target = iteration%2 ? data0 : data1;

        for (i=0; i<height; i++) {
            for (j=0; j<width; j++) {
                current = i*width + j;

                // Copy the edge pixels as is
                if (i == 0 || j == 0 || i+1 == height || j+1 == width) {
                    target[current] = source[current];
                    continue;
                }

                // Calculate the index of the cells one position up/down/left/right
                one_up    = current - width;
                one_right = current + 1;
                one_down  = current + width;
                one_left  = current - 1;

                // Calculate the weighted average and set it for the current pixel
                tmp = source[current] +
                      ((float) kappa) * (
                          source[one_up]
                          + source[one_left]
                          - 4 * source[current]
                          + source[one_right]
                          + source[one_down]
                      );

                target[current] = (int) tmp;
            }
        }
    }

    data1 = target;
    """

    data1 = copy.deepcopy(data0);

    def output(val):
        print val;

    weave.inline(
        code,
        [
            'data0',
            'data1',
            'width',
            'height',
            'kappa',
            'iterations',
            'output'
        ]
    );

    return data1;

def denoise_file(source, destination, kappa=1.0, iterations=1):
    # Load image data from input file into an numpy.ndarray
    try:
        data = np.array(Image.open(source))
    except IOError:
        print 'Source file [%s] could not be loaded.' % source;
        exit();

    # Get width and height based on the data shape
    height, width = data.shape[:2];

    # Perform denoising of image
    denoised_data = denoise_image_data(data, width, height, kappa, iterations);

    # Ouput denoised image data to new file
    try:
        Image.fromarray(denoised_data).save(destination);
    except IOError:
        print 'Destination file [%s] was not writeable.' % destination;
        exit();
