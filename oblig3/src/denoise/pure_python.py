from PIL import Image;          # Python image library

from shared import should_do_manipulation;

def denoise_image_data(data0, width, height, kappa=1, iterations=1):
    """
    Performs denoising of image data.

    Parameters
    ----------
    data0 : array
        Array containing the pixel values.
    width : int
        Image width in pixels.
    height : int
        Image height in pixels.
    kappa : float
        The denoising factor. Allowed range: [0.0-1.0]
    iterations : int
        Number of interations to do with the denoising.

    Returns
    -------
    array
        Array with the same shape as the data0 parameter containing
        manipulated image data.

    Examples
    --------
    Ensure that correct average weighted average is calculated with kappa=1.0
    >>> denoise_image_data([30, 30, 30, 30, 40, 10, 20, 40, 50, 50, 50, 50], 4, 3, 1, 1)
    [30, 30, 30, 30, 40, 110, 70, 40, 50, 50, 50, 50]

    Ensure that correct average weighted average is calculated with kappa=0.5
    >>> denoise_image_data([30, 30, 30, 30, 40, 10, 20, 40, 50, 50, 50, 50], 4, 3, 0.5, 1)
    [30, 30, 30, 30, 40, 60, 45, 40, 50, 50, 50, 50]

    Ensure that input is returned when doing no iterations
    >>> denoise_image_data([30, 30, 30, 30, 40, 10, 20, 40, 50, 50, 50, 50], 4, 3, 1, 0)
    [30, 30, 30, 30, 40, 10, 20, 40, 50, 50, 50, 50]
    """

    data = {
        'd0' : data0,                    # Input data array
        'd1' : [None] * (width * height) # Same-sized array
    };

    # Creating lists once to avoid doing it on each iteration
    i_range = range(iterations);
    y_range = range(height);
    x_range = range(width);


    # Set both source and target to d0 now, to accound for
    # the unlikely edge case where we're doing no iterations.
    # Setting the target to d1 right away would then cause
    # the array filled with Nones to be returned, which is
    # not the desired behaviour (should return the input data).
    source = data['d0'];
    target = data['d0'];

    # Do iterations
    for i in i_range:
        source = data['d1'] if i%2 else data['d0'];
        target = data['d0'] if i%2 else data['d1'];

        # Iterate over each row in the picture
        for y in y_range:

            # Iterate over each pixel in the row
            for x in x_range:

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
                target[current] = max(0, min(255, int(round(float(source[current]) + kappa*(
                                      source[one_up]
                                      + source[one_left]
                                      - 4 * source[current]
                                      + source[one_right]
                                      + source[one_down]
                                  )))));

    return target;

def denoise_file(source, destination, kappa, iterations, manipulations={}):
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

    # Check if the image is a color image
    if type(data[0]) is tuple:
        print 'Color images are not supported in the pure python backend.';
        exit();

    # Give warning if manipulation is requested
    if should_do_manipulation(manipulations):
        print 'Manipulations are not supported i C backend';
        exit();

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

if __name__ == "__main__":
    import doctest;
    doctest.testmod();