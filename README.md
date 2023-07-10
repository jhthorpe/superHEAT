# superHEAT
Repo to help with generating superHEAT calculations and tests

Note that this requires docopt has been installed, and is running python3.0 or later.

## Usage
1. Export this module's src directory into your PYTHONPATH enviroment variable
2. Modify one of the example.py files or src/template.py to generate your specific joblist
3. Modify a ZMAT and a run.dummy file to use the defined abreviations to be substituted
4. Execute this script with python3 script_name.py . Docopt can help you from there 

If you don't know the abbreviations, you can look at the bottom of src/option.py, which defines the default set of options available. Alternatively, you can print them via the Options.print() function. 

## How this works
The basic premise is that there are a list of options (some defaults, to which you can append as desired), which look for strings within your ZMAT or run.dummy files that will be replaced with some actual values later. For instance, at the start, CALC=XXX would be in your ZMAT, and zmat.0001 (or something like that) will replace that XXX with an actual calculation that you designate in your script. 

There is essentially no safeguards here, you can create and run as terrible of a ZMAT as you like. However, if you come up with a useful recipe, feel free to add it in the "examples" directory for everyone to use.

