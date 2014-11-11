def restricted_float(x):
    x = float(x);

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,));

    return x;

def should_do_manipulation(manipulations):
	if manipulations == {}:
		return False;

	if manipulations['lr'] != 0 or manipulations['lg'] != 0 or manipulations['lb'] != 0:
		return True;

	if manipulations['lh'] != 0 or manipulations['ls'] != 0 or manipulations['li'] != 0:
		return True;

	return False;