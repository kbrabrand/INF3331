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
        denoised.H = fmax(0, fmin(359, roundf((float) current.H + kappa * (
            one_up.H
            + one_left.H
            - 4 * current.H
            + one_right.H
            + one_down.H
        ))));

        // Saturation
        denoised.S = fmax(0, fmin(1, current.S + kappa * (
            one_up.S
            + one_left.S
            - 4 * current.S
            + one_right.S
            + one_down.S
        )));

        // Intensity
        denoised.I = fmax(0, fmin(1, current.I + kappa * (
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
    float tmp_val;

    // Variables to store index positions in
    int current, one_up, one_right, one_down, one_left;

    // Pointers to use when performing the denoising
    npy_ubyte* tmp;

    // HSI and RGB variables
    HSI current_HSI, one_up_HSI, one_right_HSI, one_down_HSI, one_left_HSI;
    HSI denoised_HSI;
    HSI hsi;
    RGB rgb;
    int r, g, b;

    // Do dem iterations
    for (iteration=0; iteration<iterations; iteration++) {

        for (i=0; i<height; i++) {

            for (j=0; j<width; j++) {

                // Calculate index of current pixel
                current = (i * width + j) * channels;

                // Copy the edge pixels as is
                if (i == 0 || j == 0 || i+1 == height || j+1 == width) {

                    // Copy the edge pixel as is
                    data1[current] = data0[current];

                    // If we're working on a color image, we need to copy the
                    // G and B component as well
                    if (channels == 3) { // RGB
                        data1[current + 1] = data0[current + 1];
                        data1[current + 2] = data0[current + 2];
                    }

                    // Skip to next round to avoid doing the processing we're not
                    // supposed to do for the edge pixels
                    continue;
                }

                // Calculate the index of the cells one position up/down/left/right
                one_up    = current - (width * channels);
                one_right = current + channels;
                one_down  = current + (width * channels);
                one_left  = current - channels;

                // Some extra magic for the color images
                if (channels == 3) { // RGB

                    current_HSI    = createHSIFromRGB(data0[current], data0[current+1], data0[current+2]);
                    one_up_HSI     = createHSIFromRGB(data0[one_up], data0[one_up+1], data0[one_up+2]);
                    one_right_HSI  = createHSIFromRGB(data0[one_right], data0[one_right+1], data0[one_right+2]);
                    one_down_HSI   = createHSIFromRGB(data0[one_down], data0[one_down+1], data0[one_down+2]);
                    one_left_HSI   = createHSIFromRGB(data0[one_left], data0[one_left+1], data0[one_left+2]);

                    // Calculate denoised HSI values
                    denoised_HSI   = calculated_denoised_HSI(
                        current_HSI,
                        one_up_HSI,
                        one_right_HSI,
                        one_down_HSI,
                        one_left_HSI,
                        kappa
                    );

                    // Convert HSI back to RGB
                    rgb = createRGBFromHSI(denoised_HSI);

                    // Set the values back on the different components of the pixel
                    data1[current]   = rgb.R;
                    data1[current+1] = rgb.G;
                    data1[current+2] = rgb.B;

                } else { // MONOCHROME

                    // Calculate the weighted average and set it for the current pixel
                    data1[current] = (int) roundf((float) data0[current] +
                          kappa * (
                              data0[one_up]
                              + data0[one_left]
                              - 4 * data0[current]
                              + data0[one_right]
                              + data0[one_down]
                          ));
                }
            }
        }

        // Swap pointers before next iteration
        tmp = data0;
        data0 = data1;
        data1 = tmp;
    }

    // Swap pointers back if we did an odd number of iterations
    if (iterations && iteration%2) {
        tmp = data0;
        data0 = data1;
        data1 = tmp;
    }

    // If this is a color image, we might be doing some channel manipulation
    if (channels == 3) {

        for (i=0; i<height; i++) {

            for (j=0; j<width; j++) {

                // Calulcate position of current pixel
                current = ((i*width) + j) * channels;

                // Get the r, g and b component
                r = data1[current];
                g = data1[current + 1];
                b = data1[current + 2];

                // Do conversion to/from HSI if the user specified a manipulation
                // on one of the channels (H, S or I)
                if (man_h != 0 || man_s != 0 || man_i != 0) {

                    // Convert to HSI
                    hsi = createHSIFromRGB(r, g, b);

                    // Add the desired manipulation value and ensure within bounds
                    hsi.H = fmax(0, fmin(359, hsi.H + man_h));
                    hsi.I = fmax(0, fmin(1, hsi.I + man_i));
                    hsi.S = fmax(0, fmin(1, hsi.S + man_s));

                    // Convert back to RGB
                    rgb = createRGBFromHSI(hsi);

                    // Set manipulated values
                    r = rgb.R;
                    g = rgb.G;
                    b = rgb.B;
                }

                // Set manipulated pixel values
                data1[current]     = fmax(0, fmin(255, r + man_r));
                data1[current + 1] = fmax(0, fmin(255, g + man_g));
                data1[current + 2] = fmax(0, fmin(255, b + man_b));
            }
        }
    }
""";