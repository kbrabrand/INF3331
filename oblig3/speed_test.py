from timeit import timeit;

# Set up paths
scripts   = ['pure_python', 'numpy_weave', 'denoise_c'];
test_file = 'assets/disasterbefore.jpg';
out_file  = 'tmp/out.jpg';

# Set up test params
kappa 	   = 0.1;
iterations = 5;
executions = 10;

print "Denoising %s %d times, \nwith kappa=%f and %d iterations \
per execution.\n" % (test_file, executions, kappa, iterations);

print "(execution times shown are totals)\n";

# Get length of longest script name
script_name_length = len(max(scripts, key=len));

# Perform the test once for each script
for script in scripts:
	setup = "from src.denoise.%s import denoise_file" % script;
	codeline = "denoise_file(\"%s\", \"%s\", %f, %d)" % (test_file, out_file, kappa, iterations);

	# Prepare padded script name, for prettier output
	padded_script_name = script.ljust(script_name_length);

	# Perform timing of script
	execution_time 	   = timeit(codeline, setup, number=executions);

	# Output result
	print "%s: %f seconds" % (padded_script_name, execution_time);
