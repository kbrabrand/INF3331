#!/usr/bin/env python

import random   # Random number generator
import os       # Crossplatform OS rutines
import sys      # interpreter tools
import time     # Time lib


legal_chars = "abcdefghijklmnopqrstuvwxyz"+\
              "ABCDEFGHIJKLMNOPQRSTUVWXYZ"+\
              "0123456789_"


def random_string(length=6, prefix="", legal_chars=legal_chars):
    """
Create a random string of text.

Parameters
----------
length : int
    Length of the string (minus the prefix part).
prefix : string
    Prefix the string with some text.
legal_chars : string
    A string of charracter that are allowed to be used in the
    output.

Returns
-------
rnd_str : str
    A string of random charracters.
    """
    return prefix + "".join(random.choice(legal_chars) for _ in range(length))

def generate_tree(target, dirs=3, rec_depth=2, verbose=False):
    """
Genereate a random folder structure with random names.

Parameters
----------
target : str
    Path to the root where folders are to be created.
dirs : int
    Maximum number of directories to be created per directory.
rec_depth : int
    Maximum directory depth.
verbose : bool
    Be loud about what to do.
    """

    try:
        os.stat(target)

        if verbose: print "[DIR]  %s exists" % target
    except:
        os.mkdir(target)

        if verbose: print "[DIR]  %s created" % target

    if rec_depth > 0:
        for _ in range(random.randint(0, dirs)):
            generate_tree(random_string(random.randint(1, 16), target + "/"), dirs, rec_depth - 1, verbose)

def create_file(filepath, size, start_time, end_time, verbose):
    """
Generate random file with random content

Parameters
----------
filepath : str
    Path to the file to create
size : int
    Maximum size in kilobyte for each file.
start_time : int
    Lower bound for access time (atime) and modified time (mtime)
    allowed in each file.
    Denoted in Unix time format.
end_time : int
    Same as start_time, but for upper bound.
verbose : bool
    Be loud about what to do.
    """

    length = random.randint(1, 1024 * size)

    fo = open(filepath, "wb")
    fo.write(random_string(length));
    fo.close();

    atime = random.randint(start_time, end_time)
    mtime = random.randint(start_time, end_time)

    os.utime(filepath,(atime, mtime))

    if verbose:
        print "[FILE] %s created (a: %d, m: %d) with %d chars of gibberish" % (filepath, atime, mtime, length)


def populate_tree(target, files=5, size=800, start_time=1388534400,
        end_time=1406851201000, verbose=False):
    """
Generate random files with random content.

Parameters
----------
target : str
    Path to the file tree where the files are being created.
files : int
    Maximum number of directories to be created.
size : int
    Maximum size in kilobyte for each file.
start_time : int
    Lower bound for access time (atime) and modified time (mtime)
    allowed in each file.
    Denoted in Unix time format.
end_time : int
    Same as start_time, but for upper bound.
verbose : bool
    Be loud about what to do.
    """

    for root, dirs, _ in os.walk(target):
        for name in dirs:
            dir_path = os.path.join(root, name)

            for _ in range(random.randint(0, files)):
                file_name = random_string(random.randint(0, 16), dir_path + "/") + ".file"

                create_file(
                    file_name,
                    size,
                    start_time,
                    end_time,
                    verbose
                )

            populate_tree(dir_path, files, size, start_time, end_time, verbose);


# If-test to ensure code only executed if ran as stand-alone app.
if __name__ == "__main__":

    l = len(sys.argv)

    if l < 4:
        print "Not enough arguments included."
        print "usage: %s target dirs files " % sys.argv[0] +\
            "[size rec_depth start end seed verbose]"
        sys.exit(0)

    target = sys.argv[1]
    dirs   = int(sys.argv[2])
    files  = int(sys.argv[3])

    # And-or trick to use argv only if argv is long enough.
    size      = l<5 and 1000 or int(sys.argv[4])
    rec_depth = l<6 and 2 or int(sys.argv[5])
    start     = l<7 and 1388534400 or int(sys.argv[6])
    end       = l<8 and 1406851200 or int(sys.argv[7])
    seed      = l<9 and time.time() or int(sys.argv[8])
    verbose   = (l>9 and int(sys.argv[9]) > 0)

    # Fix the random seed (if not None):
    random.seed(seed or None)

    generate_tree(target, dirs, rec_depth, verbose)
    populate_tree(target, files, size, start, end, verbose)

