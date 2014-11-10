support_c = """
    #include <math.h>

    typedef struct {
        int H; // Hue
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
    HSI createHSIFromRGB(int int_r, int int_g, int int_b) {
        HSI hsi;

        float tmp1, tmp2;
        float r, g, b;

        // Cast all values to floats for use when doing math.
        r = (float) int_r / 255;
        g = (float) int_g / 255;
        b = (float) int_b / 255;

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
            hsi.H = roundf(acos(tmp1 / sqrt(tmp2)) * 180 / pi);
        } else {
            hsi.H = roundf(360.0 - acos(tmp1 / sqrt(tmp2)) * 180 / pi);
        }

        // Set H to 0 if it's NaN
        if (isnan(hsi.H)) {
            hsi.H = 0;
        }

        return hsi;
    }

    // Create an RGB instance based on the HSI values
    RGB createRGBFromHSI(HSI hsi) {
        RGB rgb;

        float r, g, b;

        if (hsi.H == 0) {

            r = hsi.I + 2 * hsi.I * hsi.S;
            g = hsi.I - hsi.I * hsi.S;
            b = hsi.I - hsi.I * hsi.S;

        } else if (hsi.H > 0 && hsi.H < 120) {

            r = hsi.I + (hsi.I * hsi.S * (cos(hsi.H * pi / 180) / cos((60 - hsi.H) * pi / 180)));
            g = hsi.I + (hsi.I * hsi.S * (1 - (cos(hsi.H * pi / 180) / cos((60 - hsi.H) * pi / 180))));
            b = hsi.I - hsi.I * hsi.S;

        } else if (hsi.H == 120) {

            r = hsi.I - hsi.I * hsi.S;
            g = hsi.I + 2 * hsi.I * hsi.S;
            b = hsi.I - hsi.I * hsi.S;

        } else if (hsi.H > 120 && hsi.H < 240) {

            r = hsi.I - hsi.I * hsi.S;
            g = hsi.I + (hsi.I * hsi.S * (cos((hsi.H - 120) * pi / 180) / cos((180 - hsi.H) * pi / 180)));
            b = hsi.I + (hsi.I * hsi.S * (1 - (cos((hsi.H - 120) * pi / 180) / cos((180 - hsi.H) * pi / 180))));

        } else if (hsi.H == 240) {

            r = hsi.I - hsi.I * hsi.S;
            g = hsi.I - hsi.I * hsi.S;
            b = hsi.I + 2 * hsi.I * hsi.S;

        } else if (hsi.H > 240 && hsi.H < 360) {

            r = hsi.I + (hsi.I * hsi.S * (1 - (cos((hsi.H - 240) * pi / 180) / cos((300 - hsi.H) * pi / 180))));
            g = hsi.I - hsi.I * hsi.S;
            b = hsi.I + (hsi.I * hsi.S * (cos((hsi.H - 240) * pi / 180) / cos((300 - hsi.H) * pi / 180)));

        }

        // Multiply the calculated float with 255 to get the RGB value
        // and ensure that it's within the allowed range [0:255]
        rgb.R = fmin(255, fmax(0, roundf(255 * r)));
        rgb.G = fmin(255, fmax(0, roundf(255 * g)));
        rgb.B = fmin(255, fmax(0, roundf(255 * b)));

        return rgb;
    }

    HSI calculated_denoised_HSI(HSI current, HSI one_up, HSI one_right, HSI one_down, HSI one_left, float kappa) {
        HSI denoised;

        // Hue
        denoised.H = fmax(0, fmin(360, (float) current.H + kappa * (
            one_up.H
            + one_left.H
            - 4 * current.H
            + one_right.H
            + one_down.H
        )));

        // Saturation
        denoised.S = fmax(0, fmin(1, (float) current.S + kappa * (
            one_up.S
            + one_left.S
            - 4 * current.S
            + one_right.S
            + one_down.S
        )));

        // Intensity
        denoised.I = fmax(0, fmin(255, current.I + kappa * (
            one_up.I
            + one_left.I
            - 4 * current.I
            + one_right.I
            + one_down.I
        )));

        return denoised;
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

    // HSI and RGB variables
    HSI current_HSI, one_up_HSI, one_right_HSI, one_down_HSI, one_left_HSI;
    HSI denoised_HSI;
    RGB denoised_RGB;

    for (iteration=0; iteration<iterations; iteration++) {
        // On the first, third,... iteration, use data0 as source and
        // data 1 as target. On the second, fourth and so on, do it the
        // other way around.

        source = iteration%2 ? data1 : data0;
        target = iteration%2 ? data0 : data1;

        for (i=0; i<height; i++) {
            for (j=0; j<width; j++) {

                // Calculate index of current pixel
                current = (i * width + j) * channels;

                // Copy the edge pixels as is
                if (i == 0 || j == 0 || i+1 == height || j+1 == width) {
                    target[current] = source[current];

                    if (channels == 3) { // RGB
                        target[current + 1] = source[current + 1];
                        target[current + 2] = source[current + 2];
                    }

                    continue;
                }

                // Calculate the index of the cells one position up/down/left/right
                one_up    = current - (width * channels);
                one_right = current + channels;
                one_down  = current + (width * channels);
                one_left  = current - channels;

                if (channels == 3) { // RGB
                    current_HSI    = createHSIFromRGB(source[current], source[current+1], source[current+2]);
                    one_up_HSI     = createHSIFromRGB(source[one_up], source[one_up+1], source[one_up+2]);
                    one_right_HSI  = createHSIFromRGB(source[one_right], source[one_right+1], source[one_right+2]);
                    one_down_HSI   = createHSIFromRGB(source[one_down], source[one_down+1], source[one_down+2]);
                    one_left_HSI   = createHSIFromRGB(source[one_left], source[one_left+1], source[one_left+2]);

                    denoised_HSI   = calculated_denoised_HSI(
                        current_HSI,
                        one_up_HSI,
                        one_right_HSI,
                        one_down_HSI,
                        one_left_HSI,
                        kappa
                    );

                    denoised_RGB = createRGBFromHSI(denoised_HSI);

                    target[current]   = denoised_RGB.R;
                    target[current+1] = denoised_RGB.G;
                    target[current+2] = denoised_RGB.B;

                } else { // MONOCHROME

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
    }

    data1 = target;
""";