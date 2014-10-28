#!/usr/bin/env python

import argparse;
from PIL import Image;

def denoise_image_data(data, width, height, kappa=1, iterations=1):
    for y in range(height):
        for x in range(width):
            if y == 0 or x == 0 or y+1 == height or x+1 == width:
                continue;

            # Calculate index of current cell
            current = (y * width) + x;

            # Calculate the index of the cells one position up/down/left/right
            one_up    = current - width;
            one_right = current + 1;
            one_down  = current + width;
            one_left  = current - 1;

            data[current]  = data[current] + \
                              kappa*(
                                  data[one_up]
                                  + data[one_left]
                                  - 4 * data[current]
                                  + data[one_right]
                                  + data[one_down]
                              );


    # Check if we're supposed to do multiple iterations
    if iterations > 1:

        print 'recurse';

        # Process the processed data. We're passing in the
        # iterator-1 in order to stop the recursion at some
        # point (when iterations =< 1)
        return denoise_image_data(
            data,
            width,
            height,
            kappa,
            (iterations - 1)
        );

    return data;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    image = Image.open('disasterbefore.jpg');
    data  = list(image.getdata());

    # Get image dimensions
    width, height = image.size;

    denoised_data = denoise_image_data(data, width, height, 1, 5);

    im = Image.new("L", (width, height))
    im.putdata(denoised_data)
    im.save("disaster_after.jpg")
