# rubric.py

# trees.txt - testing

# zip all .py files

# plus brief description of program, and method of solution

# email and blackboard



# read a file

# genreate three-letter abbrevs:

# Data Clean stage:
    # uppercase

    # ignore: apostrophes ' 
    # Other chars (nonletter) ignored, but split name into separate words. 
    # (replace with a space then?)

# Valid abbrevs:
    # must be first letter of name, plus any two others IN ORDER
    # (assume first char is a letter always)
    # exclude any abbrev. that are formed by any other names
    # but note - must be any other names...not others for this 
    # name only 
    # also in the list, so ALL duplicates go. 
    # Compile ALL possibles and lookup initially?
# score for abbrevs:
    # i) add index of containing word.
    # ii) add 10 for voewl in abbrev, unless first letter in word
    # iii) some abbrevs can be formed more than one way: lowest shoule
    # be chosen. 

# need one main function , the calling Fn.
# should prompt for name of file, write to FILENAME_abbrevs.txt
# see sheet for correct output but esentially:
# Cold
# CLD
# Cool
# COO
# C++ Code
# CCD
# Unpossible Example
# ****left blank****
# Multiple Best Equal Answers
# MBEA MUBE MTAR etc
