import argparse;

def restricted_float(x):
    """
    Checks if a float is between 0.0 and 1.0.

    Parameters
    ----------
    x : float
    	Float to check

    Returns
    -------
    mixed
    	Returns float or raises an exception.

    Examples
    --------
    Returns input value if valid
    >>> restricted_float(0.5)
    0.5

    Raises exception if lower than allowed
    >>> restricted_float(-0.5)
    Traceback (most recent call last):
    ...
    ArgumentTypeError: -0.5 not in range [0.0, 1.0]

    Raises exception if higher than allowed
    >>> restricted_float(1.5)
    Traceback (most recent call last):
    ...
    ArgumentTypeError: 1.5 not in range [0.0, 1.0]
    """

    x = float(x);

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,));

    return x;

def should_do_manipulation(manipulations):
	"""
	Checks if provided dict contains a key that indicates
	that manipulations should be done.

	Parameters
	----------
	manipulations : dict
		Dictionary containing keys for the different components

	Returns
	-------
	bool
		Whether or not manipulations should be done

	Examples
	--------
	Returns False on empty dict
	>>> should_do_manipulation({})
	False

	Returns False when lr is present and equal to zero
	>>> should_do_manipulation({'lr':0})
	False

	Returns True when lr is present and not equal to zero
	>>> should_do_manipulation({'lr': 1})
	True

	Returns False when lg is present and equal to zero
	>>> should_do_manipulation({'lg':0})
	False

	Returns True when lg is present and not equal to zero
	>>> should_do_manipulation({'lg': 1})
	True

	Returns False when lb is present and equal to zero
	>>> should_do_manipulation({'lb':0})
	False

	Returns True when lb is present and not equal to zero
	>>> should_do_manipulation({'lb': 1})
	True

	Returns False when lh is present and equal to zero
	>>> should_do_manipulation({'lh':0})
	False

	Returns True when lh is present and not equal to zero
	>>> should_do_manipulation({'lh': 1})
	True

	Returns False when ls is present and equal to zero
	>>> should_do_manipulation({'ls':0})
	False

	Returns True when ls is present and not equal to zero
	>>> should_do_manipulation({'ls': 1})
	True

	Returns False when li is present and equal to zero
	>>> should_do_manipulation({'li':0})
	False

	Returns True when li is present and not equal to zero
	>>> should_do_manipulation({'li': 1})
	True


	Returns False when lr is present and equal to zero
	>>> should_do_manipulation({'lr':0})
	False

	Returns True when lr is present and not equal to zero
	>>> should_do_manipulation({'lr':1})
	True
	"""

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

if __name__ == "__main__":
    import doctest;
    doctest.testmod();