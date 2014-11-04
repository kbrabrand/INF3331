#!/usr/bin/env python

import argparse;
from PIL import Image;

def denoise_image_data(data, width, height, kappa=1, iterations=1):
    # Create an array for the denoised data
    denoised_data = [None] * (width * height);

    source = data;
    target = denoised_data;

    for i in range(iterations):
        if i%2 == 0:
            source = data;
            target = denoised_data;
        else:
            target = data;
            source = denoised_data;

        for y in range(height):
            for x in range(width):
                # Calculate index of current cell
                current = (y * width) + x;

                # We're not manipulating the edge pixels
                if y == 0 or x == 0 or y+1 == height or x+1 == width:
                    target[current] = source[current];
                    continue;

                # Calculate the index of the cells one position up/down/left/right
                one_up    = current - width;
                one_right = current + 1;
                one_down  = current + width;
                one_left  = current - 1;

                # Get the weighted average and set it for the current pixel
                target[current] = source[current] + \
                                  kappa*(
                                      source[one_up]
                                      + source[one_left]
                                      - 4 * source[current]
                                      + source[one_right]
                                      + source[one_down]
                                  );

    return target;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    image = Image.open('disasterbefore.jpg');
    data  = list(image.getdata());

    # Get image dimensions
    width, height = image.size;

    denoised_data = denoise_image_data(data, width, height, 0.2, 1);

    im = Image.new("L", (width, height))
    im.putdata(denoised_data)
    im.save("disaster_after.jpg")
