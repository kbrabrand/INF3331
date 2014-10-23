Oblig 2
==================

#Documentation
Explanation of tasks can be found in reports/[oblig1.tex](https://github.com/UiO-INF3331/INF3331-Kristoffer/tree/master/oblig2/report/oblig2.tex)/[pdf](https://github.com/UiO-INF3331/INF3331-Kristoffer/tree/master/oblig2/report/oblig2.pdf) and in the inline comments.

#Usage
To preprocess and compile a file, issue the following command

```bash
python prepro.py input-file.tex output-file-tex.tex
python compile output-file.tex
```

#Tests
Doctests for internal functions in the preprocessor. Test suites for the larger blocks of the application.

The tests suites can be run using nose;

```bash
nosetest
```

– Kristoffer