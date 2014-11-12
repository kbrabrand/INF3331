import numpy as np;
import Image;
from sys import argv;

from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;
from src.denoise.denoise_c   import denoise_file as c_denoise;

# Set up paths
scripts   = ['numpy_weave', 'c', 'python'];
test_file = 'assets/disasterbefore.jpg';

# Set up test params
kappas 	   = [0.1, 0.2];
iterations = [5, 10];

# Dict for tmp image data
image_data = {};

for kappa in kappas:

	image_data[kappa] = {};

	for iter in iterations:

		image_data[kappa][iter] = {};

		for script in scripts:

			denoiser = locals()["%s_denoise" % script];

			output_file_name = 'tmp/%s-%f-%d.jpg' % (script, kappa, iter);

			# Denoise files
			denoiser(
				test_file,
				output_file_name,
				kappa,
				iter,
				{},
				False
			);

			# Get image data
			image_data[kappa][iter][script] = np.array(Image.open(output_file_name));

eps = int(argv[1]) if len(argv) > 1 else 2;
highest_error = 0;
tmp_min = 0;
tmp_max = 0;
successfull_pixels = 0;
failed_pixels = 0;

# Check image data
for kappa in image_data:

	for iter in image_data[kappa]:

		scripts = image_data[kappa][iter].keys();

		shape = image_data[kappa][iter][scripts[0]].shape;

		for y in range(shape[0]):
			for x in range(shape[1]):
				tmp_min = int(min(
					image_data[kappa][iter]['c'][y][x],
					image_data[kappa][iter]['numpy_weave'][y][x],
					image_data[kappa][iter]['python'][y][x]
				));

				tmp_max = int(max(
					image_data[kappa][iter]['c'][y][x],
					image_data[kappa][iter]['numpy_weave'][y][x],
					image_data[kappa][iter]['python'][y][x]
				));

				highest_error = max(highest_error, (tmp_max - tmp_min));

				if (tmp_max - tmp_min) > eps:
					# print 'oh no... Diff: %d' % (tmp_max - tmp_min);
					# print 'kappa: %f, iter: %d, x: %d, y: %d' % (kappa, iter, x, y);

					failed_pixels += 1;
				else:
					successfull_pixels += 1;

print 'successfull: %d' % successfull_pixels;
print 'failed: %d' % failed_pixels;

error_rate = float(failed_pixels) / (successfull_pixels + failed_pixels);

if failed_pixels == 0:
	print 'The variation between the different backends \nwere all within the specified EPS (%d)' % eps;
else:
	print '%f percent of the pixels had a greater variation than the\nspecified EPS (%d)' % (error_rate * 100, eps);