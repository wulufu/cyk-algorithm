# ICSI 409 CYK Algorithm
Wolfgang Neal, Alex Bailey, Collin Smith, Ishtyaq Khan, Jack Arevalo

## Table of Contents
- [Description](#description)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contributions](#contributions)

## Description
This script creates a context-free grammar from a text file and uses it to
perform CYK on strings. The path for this file can be provided using '-c' or
'--cfg' when running the script, otherwise the user will be prompted for it.
Additionally, a file containing a list of strings to test can be provided
using '-t' or '--test'. The program will exit if any file is not found.

Each line in the CFG file must be of the form "A -> BC", "S -> epsilon", or
"A -> a", where 'A', 'B', and 'C' are variables, 'S' is the axiom, and 'a' is
a terminal. Optionally, two or more rules with the same left-hand side can be
combined into one line using the form "A -> BC | a".

A variable that appears on the right-hand side of a rule must also be
defined on the left-hand side of at least one rule. The first variable
to be defined is assumed to be the axiom of the CFG. If any rule in the file
is formatted incorrectly, the program will exit.

If a test file has been provided, the results from performing CYK on the
strings found within the file will be displayed. Each line in the file is
treated as an individual string.

Otherwise, with no test file, the user will be prompted to enter a string.
CYK will be performed on this string, and the result will be displayed.
This will repeat indefinitely until the program is terminated.

## Dependencies
- Python 3.12

## Usage
- ```python cyk.py```
  The program will start by asking for the path of a file containing a context-free grammar.
- ```python cyk.py -c <FILE>```
  Replace `<FILE>` with the path of a file containing a context-free grammar.
- ```python cyk.py -t <FILE>```
  Replace `<FILE1>` with the path of a file containing strings to test on a context-free grammar. The program will
  start by asking for the name of a file containing a context-free
  grammar to test these strings on.
- ```python cyk.py -c <FILE1> -t <FILE2>```
  Replace `<FILE1>` with the path of a file containing a context-free grammar. Replace `<FILE2>` with the path of a
  file containing strings to test on that grammar.

The test files provided contain 6 strings each. The first 3 are strings that will be accepted by the file's
corresponding set of rules, while the last 3 won't be accepted.

## Contributions
1. Production of grammars and conversion to CNF on paper: Alex Bailey
2. Implementation and preliminary testing: Wolfgang Neal and Ishtyaq Khan
3. Testing and documentation: Collin Smith and Jack Arevalo
