def restricted_float(x):
    x = float(x);

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,));

    return x;

def should_do_manipulation(manipulations):
	if manipulations == {}:
		return False;

	if 'lr' in manipulations.keys() and manipulations['lr'] != 0:
		return True;

	if 'lg' in manipulations.keys() and manipulations['lg'] != 0:
		return True;

	if 'lb' in manipulations.keys() and manipulations['lb'] != 0:
		return True;

	if 'lh' in manipulations.keys() and manipulations['lh'] != 0:
		return True;

	if 'ls' in manipulations.keys() and manipulations['ls'] != 0:
		return True;

	if 'li' in manipulations.keys() and manipulations['li'] != 0:
		return True;

	return False;