import cProfile, pstats, StringIO;
import re;

from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;

denoisers = ['python_denoise', 'numpy_weave_denoise'];

# Set up paths
test_file = 'assets/disasterbefore.jpg';
out_file  = 'tmp/out.jpg';

# Set up test params
kappa 	   = 0.1;
iterations = 5;
executions = 10;

print "Denoising %s %d times, \nwith kappa=%f and %d iterations \
per execution.\n" % (test_file, executions, kappa, iterations);

# Perform the test once for each script
for denoiser in denoisers:
	# Retrieve function from symbol table
	function_to_profile = locals()[denoiser];

	pr = cProfile.Profile();
	pr.enable();

	# Execute function
	function_to_profile(test_file, out_file, kappa, iterations);

	pr.disable();

	s = StringIO.StringIO();
	ps = pstats.Stats(pr, stream=s).sort_stats('cumulative');
	ps.print_stats();

	print "\n\n==================================================";
	print '{:=^50}'.format(" " + denoiser + " ");
	print "==================================================";

	print "\n".join(s.getvalue().splitlines()[4:8]);