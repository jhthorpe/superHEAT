# superHEAT

This repo is designed to facilitate the generation and investigation of theoretical model chemistries, and to serve as a curated dataset for quantum chemical calculations on species of interest. A brief description of the various modules and capabilities is given below. Each source file has a more detailed description, and examples for users are given in the examples directory.  


## Installation
Note that the archive is (and must always be) zipped on the Git repo. The `zip_archive.py` and `unzip_archive.py` scripts are given as an OS independent way of performing these actions, and you will need to zip the archive before you can commit it, and unzip it before you can use it. 

To install the package itself, use `python3 -m pip install .` I have not yet finished the development of this package as a general enviroment, but you can see how to use the various features by looking in the examples folder. 

## Dependencies
- docopt (*https://github.com/docopt/docopt*)
- python3.0 or later
- numpy
- scipy
- pytest

## Archive Manager
A package that is used to archive data useful in developing theoretical model chemistries. See `examples/archive_manager` for some demonstrations of the capabilities. Currently, there are the following archives that are tracked:

- constarc : an archival system for tracking defintions of constants and units used in various litterature or program packages. 

## Script Generator 
Package to help with generating superHEAT calculations and tests. See `examples/script_generator` for how to construct your own scripts that use this.  

**Viewing joblist**
`python3 script_name.py --joblist`

**Viewing Substitution Variables**
`python3 script_name.py --abrvs`

**Generating files**
1. Modify one of the example.py files or src/template.py to generate your specific joblist.
2. Modify a ZMAT and a run.dummy file to use the defined abreviations to be substituted.
3. Execute this script with `python3 script_name.py .` Docopt can help you from there. 

If you don't know the abbreviations, you can look at the bottom of `src/script_generator/option.py`, which defines the default set of options available. Alternatively, you can print them via the `Options.print()` function. 

### How this works
The basic premise is that there are a list of options (some defaults, to which you can append as desired), which look for strings within your ZMAT or run.dummy files that will be replaced with some actual values later. For instance, at the start, CALC=XXX would be in your ZMAT, and zmat.0001 (or something like that) will replace that XXX with an actual calculation that you designate in your script. 

There is essentially no safeguards here, you can create and run as terrible of a ZMAT as you like. However, if you come up with a useful recipe, feel free to add it in the "examples" directory for everyone to use.

