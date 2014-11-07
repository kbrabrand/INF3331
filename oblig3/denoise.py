import argparse;
from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;
from src.denoise.shared      import restricted_float;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    parser = argparse.ArgumentParser();

    parser.add_argument('source',  	    metavar='src', help='Path to source image');
    parser.add_argument('destination',  metavar='dst', help='Destination for output image');
    parser.add_argument('--denoiser',   metavar='denoiser', default="numpy_weave", choices=['python', 'numpy_weave'], help='What denoiser to use');
    parser.add_argument('--denoise',    default=False, help='Perform denoising of image', action='store_true');
    parser.add_argument('--kappa',      metavar='K', type=restricted_float, default=0.1, help="Kappa value. Allowed range [0.0, 1.0]");
    parser.add_argument('--iterations', metavar='I', type=int, default=10, help='Number of iterations to run with the denoiser.');
    parser.add_argument('--eps', 		metavar='E', type=int, default=2, help="Fault tolerance");

    args = parser.parse_args();

    # Get denoiser function from local symbol table
    denoiser = locals()[args.denoiser + "_denoise"];

    # Perform denoising
    denoiser(args.source, args.destination, args.kappa, args.iterations);