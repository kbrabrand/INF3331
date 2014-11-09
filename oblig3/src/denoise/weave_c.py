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

    // Value for pi, used in the math below
    float pi = 3.14159256;

    // Create an HSI instance based on the RGB values
    HSI createHSIFromRGB(RGB rgb) {
        HSI hsi;

        float tmp1, tmp2;
        float r, g, b;

        // Cast all values to floats for use when doing math.
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
            hsi.H = acos(tmp1 / sqrt(tmp2)) * 180 / pi;
        } else {
            hsi.H = 360.0 - acos(tmp1 / sqrt(tmp2)) * 180 / pi;
        }

        return hsi;
    }

    // Create an RGB instance based on the HSI values
    RGB createRGBFromHSI(HSI hsi) {
        RGB rgb;

        // H == 0
        if (hsi.H == 0) {
            rgb.R = roundf(hsi.I + 2 * hsi.I * hsi.S);
            rgb.G = roundf(hsi.I - hsi.I * hsi.S);
            rgb.B = roundf(hsi.I - hsi.I * hsi.S);
        }

        // 0 > H < 120
        if (hsi.H > 0 && hsi.H < 120) {
            rgb.R = roundf(hsi.I + (hsi.I * hsi.S * (cos(hsi.H * pi / 180) / cos((60 - hsi.H) * pi / 180))));
            rgb.G = roundf(hsi.I + (hsi.I * hsi.S * (1 - (cos(hsi.H * pi / 180) / cos((60 - hsi.H) * pi / 180)))));
            rgb.B = roundf(hsi.I - hsi.I * hsi.S);
        }

        // H == 120
        if (hsi.H == 120) {
            rgb.R = roundf(hsi.I - hsi.I * hsi.S);
            rgb.G = roundf(hsi.I + 2 * hsi.I * hsi.S);
            rgb.B = roundf(hsi.I - hsi.I * hsi.S);
        }

        // 120 > H < 240
        if (hsi.H > 120 && hsi.H < 240) {
            rgb.R = roundf(hsi.I - hsi.I * hsi.S);
            rgb.G = roundf(hsi.I + (hsi.I * hsi.S * (cos((hsi.H - 120) * pi / 180) / cos((180 - hsi.H) * pi / 180))));
            rgb.B = roundf(hsi.I + (hsi.I * hsi.S * (1 - (cos((hsi.H - 120) * pi / 180) / cos((180 - hsi.H) * pi / 180)))));
        }

        // H == 240
        if (hsi.H == 240) {
            rgb.R = roundf(hsi.I - hsi.I * hsi.S);
            rgb.G = roundf(hsi.I - hsi.I * hsi.S);
            rgb.B = roundf(hsi.I + 2 * hsi.I * hsi.S);
        }

        // 240 > H < 360
        if (hsi.H > 240 && hsi.H < 360) {
            rgb.R = roundf(hsi.I + (hsi.I * hsi.S * (1 - (cos((hsi.H - 240) * pi / 180) / cos((300 - hsi.H) * pi / 180)))));
            rgb.G = roundf(hsi.I - hsi.I * hsi.S);
            rgb.B = roundf(hsi.I + (hsi.I * hsi.S * (cos((hsi.H - 240) * pi / 180) / cos((300 - hsi.H) * pi / 180))));
        }

        return rgb;
    }

    // Create RGB instance from three int values (r, g and b)
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

    true;

    data1 = target;
""";