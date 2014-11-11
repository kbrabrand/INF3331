import argparse;
from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;
from src.denoise.denoise_c   import denoise_file as c_denoise;
from src.denoise.shared      import restricted_float;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    parser = argparse.ArgumentParser();

    parser.add_argument('source',  	    metavar='src', help='Path to source image');
    parser.add_argument('destination',  metavar='dst', help='Destination for output image');
    parser.add_argument('--denoiser',   metavar='denoiser', default="numpy_weave", choices=['python', 'numpy_weave', 'c'], help='What denoiser to use');
    parser.add_argument('--denoise',    metavar='D', type=int, default=1, help='Perform denoising of image', choices=[0, 1]);
    parser.add_argument('--kappa',      metavar='K', type=restricted_float, default=0.1, help="Kappa value. Allowed range [0.0, 1.0]");
    parser.add_argument('--iterations', metavar='I', type=int, default=10, help='Number of iterations to run with the denoiser.');
    parser.add_argument('--eps', 		metavar='E', type=int, default=2, help="Fault tolerance");

    parser.add_argument('-lr', metavar='N', type=int, help='Amount to add to or remove from the R channel (RGB).', default=0);
    parser.add_argument('-lg', metavar='N', type=int, help='Amount to add to or remove from the G channel (RGB).', default=0);
    parser.add_argument('-lb', metavar='N', type=int, help='Amount to add to or remove from the B channel (RGB).', default=0);
    parser.add_argument('-lh', metavar='N', type=int, help='Amount to add to or remove from the H component (HSI).', default=0.0);
    parser.add_argument('-ls', metavar='N', type=float, help='Amount to add to or remove from the S component (HSI).', default=0.0);
    parser.add_argument('-li', metavar='N', type=float, help='Amount to add to or remove from the I component (HSI).', default=0.0);

    args = parser.parse_args();

    # Set iterations to 0 if denoising is disabled
    iterations = args.iterations if args.denoise else 0;

    # Get denoiser function from local symbol table
    denoiser = locals()[args.denoiser + "_denoise"];

    # Perform denoising
    denoiser(
        args.source,
        args.destination,
        args.kappa,
        iterations,
        {
            'lr': args.lr, 'lg': args.lg, 'lb': args.lb,
            'lh': args.lh, 'ls': args.ls, 'li': args.li
        }
    );