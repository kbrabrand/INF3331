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
Doctests for internal functions in the preprocessor. Test suites for the larger blocks of the application.

The tests suites can be run using nose;

```bash
$ nosetest
```

– Kristoffer
