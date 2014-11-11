from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;
from src.denoise.denoise_c   import denoise_file as c_denoise;

# Set up paths
scripts   = ['python', 'numpy_weave', 'c'];
test_file = 'assets/disasterbefore.jpg';

# Set up test params
kappas 	   = [0.1, 0.2];
iterations = [5, 10];

# Perform the test once for each script
for script in scripts:
	denoiser = locals()["%s_denoise" % script];

	for kappa in kappas:

		for iter in iterations:

			# Denoise files
			denoiser(
				test_file,
				'tmp/%s-%f-%d.jpg' % (script, kappa, iter),
				kappa,
				iter,
				{},
				False
			);

			# Add file data to array with pixel data

# Iterate through pixel data for all backends and compare