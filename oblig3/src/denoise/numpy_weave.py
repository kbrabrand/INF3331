import numpy as np;      # NumPy
import copy;             # Tool for copying objects/arrays
from PIL import Image;   # Python image library
from scipy import weave; # Weave. For C, you know..

#from src.denoise import shared; # Shared logic for denoise

support_c = """
    #include <math.h>

    typedef struct {
        float H; // Hue
        float S; // Saturation
        float I; // Intensity
    } HSI;

    typedef struct {
        int R; // Red
        int G; // Green
        int B; // Blue
    } RGB;

    HSI createHSIFromRGB(RGB rgb) {
        HSI hsi;

        float tmp1, tmp2;
        float r, g, b;

        // Cast all values to floats for use when doing maths.
        r = (float) rgb.R;
        g = (float) rgb.G;
        b = (float) rgb.B;

        // Calculate intensity
        hsi.I = (r + g + b) / 3;

        // Calculate saturation
        if (hsi.I > 0) {
            hsi.S = 1 - (fmin(fmin(r, g), b)/hsi.I);
        } else {
            hsi.S = 0;
        }

        // Calculate hue
        tmp1 = r - g/2 - b/2;

        tmp2 = pow(r, 2) + pow(g, 2) + pow(b, 2);
        tmp2 -= r*g + r*b + g*b;

        if (g >= b) {
            hsi.H = acos(tmp1/sqrt(tmp2))*180/3.14159256;
        } else {
            hsi.H = 360.0 - acos(tmp1/sqrt(tmp2))*180/3.14159256;
        }

        return hsi;
    }

    RGB* createRGBFromHSI(HSI* hsi) {

    }

    RGB createRGB(int r, int g, int b) {
        RGB rgb;

        rgb.R = r;
        rgb.G = g;
        rgb.B = b;

        return rgb;
    }
""";

denoise_c = """
    int i, j, iteration;

    // Temporary value variable
    float tmp;

    // Variables to store index positions in
    int current, one_up, one_right, one_down, one_left;

    // Pointers to use when performing the denoising
    npy_ubyte *source, *target;

    // Set the source and target pointers
    source = data0;
    target = data0;

    for (iteration=0; iteration<iterations; iteration++) {
        // On the first, third,... iteration, use data0 as source and
        // data 1 as target. On the second, fourth and so on, do it the
        // other way around.

        source = iteration%2 ? data1 : data0;
        target = iteration%2 ? data0 : data1;

        for (i=0; i<height; i++) {
            for (j=0; j<width; j++) {
                // Calculate index of current pixel
                current = i*width*channels + j*channels;

                // Copy the edge pixels as is
                if (i == 0 || j == 0 || i+1 == height || j+1 == width) {
                    target[current] = source[current];
                    continue;
                }

                // Calculate the index of the cells one position up/down/left/right
                one_up    = current - width*channels;
                one_right = current + 1*channels;
                one_down  = current + width*channels;
                one_left  = current - 1*channels;

                // Calculate the weighted average and set it for the current pixel
                tmp = source[current] +
                      kappa * (
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
""";

def denoise_image_data(data0, width, height, kappa=1.0, iterations=1):
    # Get number of channels per pixel
    channels = 1;

    # If shape has more than two list items, the list is three dimensional
    # and we'll get the number of values per list in the 2nd dimension
    if len(data0.shape) > 2:
        channels = data0.shape[2];

    data1 = copy.deepcopy(data0);

    def output(val):
        print val;

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
            'output'
        ],
        support_code = support_c
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

if __name__ == "__main__":
    code1 = """
    int r, g, b;

    r = 120;
    g = 60;
    b = 90;

    RGB rgb = createRGB(r, g, b);

    HSI hsi  = createHSIFromRGB(rgb);

    return_val = hsi.I;
    """;

    print 'HSI = (19, 0.129, 0.405);';
    print weave.inline(
        code1,
        [],
        support_code = support_c,
        headers = ['<math.h>']
    );