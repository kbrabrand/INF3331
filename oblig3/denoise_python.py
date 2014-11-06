#!/usr/bin/env python

import argparse;         # Argument parser
from PIL import Image;   # Python image library

from src.denoise import shared; # Shared logic for denoise

def restricted_float(x):
    x = float(x);

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,));

    return x;

def denoise_image_data(data0, width, height, kappa=1, iterations=1):
    data = {
        'd0' : data0,                    # Input data array
        'd1' : [None] * (width * height) # Same-sized array
    };

    # Set both source and target to d0 now, to accound for
    # the unlikely edge case where we're doing no iterations.
    # Setting the target to d1 right away would then cause
    # the array filled with Nones to be returned, which is
    # not the desired behaviour (should return the input data).
    source = data['d0'];
    target = data['d0'];

    for i in range(iterations):
        source = data['d1'] if i%2 else data['d0'];
        target = data['d0'] if i%2 else data['d1'];

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
                target[current] = int(source[current] + kappa*(
                                      source[one_up]
                                      + source[one_left]
                                      - 4 * source[current]
                                      + source[one_right]
                                      + source[one_down]
                                  ));

    return target;

def denoise_file(source, destination, kappa, iterations):
    # Open image
    try:
        image = Image.open(source);
    except IOError:
        print 'Source file [%s] could not be loaded.' % source;
        exit();

    # Get pixel information from image
    data  = list(image.getdata());

    # Get image dimensions
    width, height = image.size;

    # Perform denoising of image
    denoised_data = denoise_image_data(data, width, height, kappa, iterations);

    # Ouput denoised image data to new file
    im = Image.new("L", (width, height));
    im.putdata(denoised_data);

    # Save file
    try:
        im.save(destination);
    except IOError:
        print 'Destination file [%s] was not writeable.' % args.destination;
        exit();

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    parser = argparse.ArgumentParser();

    parser.add_argument('source',  metavar='src', help='Path to source image');
    parser.add_argument('destination',  metavar='dst', help='Destination for output image');
    parser.add_argument('--kappa', metavar='K', type=shared.restricted_float, default=0.2, help="Kappa value. Allowed range [0.0, 1.0]");
    parser.add_argument('--iterations', metavar='I', type=int, default=5, help='Number of iterations to run with the denoiser.');

    args = parser.parse_args();

    # Perform denoising of file
    denoise_file(args.source, args.destination, args.kappa, args.iterations);