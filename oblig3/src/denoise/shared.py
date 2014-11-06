def valid_file(parser, arg):
    try:
    	return open(arg, r);
    except IOError:
    	parser.error("The file %s does not exist!" % arg);

def restricted_float(x):
    x = float(x);

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,));

    return x;