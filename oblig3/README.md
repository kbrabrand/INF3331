Oblig 3
==================

#Documentation
Explanation of tasks can be found in [oblig3.tex](https://github.com/UiO-INF3331/INF3331-Kristoffer/tree/master/oblig3/report/oblig3.tex) or [oblig3.pdf](https://github.com/UiO-INF3331/INF3331-Kristoffer/raw/master/oblig3/report/oblig3.pdf) in the report folder, and in the inline code comments.

#Installation
There's not much to install really, but in order to use the pure C backend (no support for color images or linear manipulation) you will first need to build the c files.

If you've got gcc and make installed it should be as easy as the following;

```bash
$ cd lib && make
```

Unless you se lots of warnings or other scary stuff when running the command you should be good to go. The interaction with the C backend is done throught the denoise.py script.

#Usage
To denoise and/or manipulate a file, issue the following command

```bash
$ python denoise.py source-file.jpg destination-file.jpg
```

#Tests
Doctests for internal functions in the denoiser backends and helper modules. As commented in the report, writing I didn't really see the point of implementing a test suite for this assignment as it would just be re-doing what's already done with the integrationtests in form of doctests on the backends.

For running the speed comparison test
```bash
$ python test_speed_test.py
```

For running the profiling
```bash
$ python test_profiling.py
```

For running the file comparison, issue the following command with an optional eps-argument following the script name.
```bash
$ python test_file_comparison.py
$ python test_file_comparison.py 5
```

– Kristoffer
