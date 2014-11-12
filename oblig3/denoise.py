import argparse;
from src.denoise.pure_python import denoise_file as python_denoise;
from src.denoise.numpy_weave import denoise_file as numpy_weave_denoise;
from src.denoise.denoise_c   import denoise_file as c_denoise;
from src.denoise.shared      import restricted_float;

# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image denoiser with image component manipulation support.');

    # Declare params
    parser.add_argument('source',  	       metavar='src', help='Path to source image');
    parser.add_argument('destination',     metavar='dst', help='Destination for output image');
    parser.add_argument('--backend',       metavar='B', default="numpy_weave", choices=['python', 'numpy_weave', 'c'], help='What backend to use');
    parser.add_argument('--denoise',       metavar='D', type=int, default=1, help='Perform denoising of image', choices=[0, 1]);
    parser.add_argument('--kappa',         metavar='K', type=restricted_float, default=0.1, help="Kappa value. Allowed range [0.0, 1.0]");
    parser.add_argument('--iter',          metavar='I', type=int, default=10, help='Number of iterations to run with the denoiser.');
    parser.add_argument('--verbose', '-v', dest='verbose', help="Enable verbose script output", action='store_true');

    # Declare manipulation params
    parser.add_argument('--lr', metavar='N', type=int, help='Amount to add to or remove from the R channel (RGB).', default=0);
    parser.add_argument('--lg', metavar='N', type=int, help='Amount to add to or remove from the G channel (RGB).', default=0);
    parser.add_argument('--lb', metavar='N', type=int, help='Amount to add to or remove from the B channel (RGB).', default=0);
    parser.add_argument('--lh', metavar='N', type=int, help='Amount to add to or remove from the H component (HSI).', default=0.0);
    parser.add_argument('--ls', metavar='N', type=restricted_float, help='Amount to add to or remove from the S component (HSI).', default=0.0);
    parser.add_argument('--li', metavar='N', type=restricted_float, help='Amount to add to or remove from the I component (HSI).', default=0.0);

    # Parse params
    args = parser.parse_args();

    # Set iterations to 0 if denoising is disabled
    iterations = args.iter if args.denoise else 0;

    # Get denoiser function from local symbol table
    backend = locals()[args.backend + "_denoise"];

    # Prepare manipulation dict
    manipulations = {
        'lr': args.lr, 'lg': args.lg, 'lb': args.lb,
        'lh': args.lh, 'ls': args.ls, 'li': args.li
    };

    # Process image
    result = backend(
        args.source,
        args.destination,
        args.kappa,
        iterations,
        manipulations,
        args.verbose
    );

    if result:
        print result;