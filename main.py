# main.py
import re

# DEBUG
import sys
sys.stdout.buffer.write(chr(9986).encode('utf8'))

import logging
logger = logging.getLogger('root')
FORMAT = "[%(lineno)s: - %(funcName)4s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

def main():
    '''main method, prompts for file from user and loads it, then 
    pass to processing'''

    # DEBUG:
    filename = 'test1'
    # text input:
    #filename = input('Please type name of a local file to process:')

    # build filename and .txt if needed:
    OUTPUT_SUFFIX = '_abbrevs.txt'
    if filename[-4:].lower() is not OUTPUT_SUFFIX[-4:]:
        filename = filename + OUTPUT_SUFFIX[-4:]
    
    # Read in the given file and generate potential abbreviations.
    # 
    all_abbrevs = list()
    orig_lines = list()
    with open(filename, encoding='utf-8') as text:
        
        for i, line in enumerate(text):
            
            # store the original lines in order, here, so we can 
            # look up by index later when we output:
            orig_lines.append(line)

            # remove unwanted characters etc:
            line = clean_text(line)
            
            # get the potential abbrevs for this line:
            all_abbrevs.append(find_abbrevs(line))


        # TODO: rewind handle
        # rewind
        #text.seek(0)
        #
        #
        #

    #DEBUG
    logger.debug(all_abbrevs)

    # print the original text, then its abbrevs.
    write_out(filename[0:-4] + OUTPUT_SUFFIX, all_abbrevs, orig_lines)


def write_out(filename, iterable_text, orig_lines):
    '''output a given filename with suffix to filesystem,
     contain original names and order plus the chosen abbreviations.
     (A blank given if no acceptable abbreviation).
     All tied, best matches should be printed together.
    '''
    with open(filename, mode='w', encoding='utf-8') as outfile:
        for i, orig_line in enumerate(orig_lines):
            outfile.write(orig_line)
            outfile.write(' '.join(iterable_text[i]))
            outfile.write('\n')

def clean_text(text):
    '''Wrangle and homogenise text data, ready for processing.
    -- remove apostrophes, convert other non alphas to spaces
    and deal with whitespace.'''
    text = text.strip().upper()

    # apostrophes should be ignored completely  
    regex_apos = re.compile("[’'`]")
    text = regex_apos.sub("", text)
    
    # any other non-alpha chars replaced with spaces:
    regex = re.compile('[^A-Z]+')
    return regex.sub(" ", text)

def find_abbrevs(line):
    ''' find all the possible abbreviations for a given line
    and return as a list, abbrevs'''

    # we calculate all possible 2 and 3rd letter
    # combinations (since first index always used
    # as 1st letter of our abbreviation!).
    # We use a nested loop; discount spaces. 
    # outer loop thus runs from 2nd letter to penultimate
    # since the last letter could not act as the 2nd letter
    # of any 3-letter abbreviations.
    result = list()
    for idx_i, val_i in enumerate(line[1:-1], start=1):
        
        # skip if the value is a space (and thus falsy):
        if val_i is not ' ':

            # stem is first two letters of an abbreviation
            stem = line[0] + val_i

            # inner loop to find the third letter of our eventual abbreviation:
            for idx_j, val_j in enumerate(line[idx_i+1:], start=idx_i+1):
                
                if val_j is not ' ':

                    abbrev = stem + val_j
                    # now we should append this abbreviation 
                    # as it is long enough:
                    result.append(abbrev)
                    
        
    # TODO remove duplicates
    # TODO append a tuple with indices and score also.
    
    return result


def search_value(search, list):
    '''finds searched values in a list
    and returns a list of indices for those values'''
    result = []
    [result.append(i) for i, value in enumerate(list) if value == search]
    return result
    
    # list = ['foo', 'bar', 'baz', 'foo']
    # search = 'foo'
    # logger.debug(search_value(search, list))

    # if list.count(search):
    #     return list.index(search)
    
    # if search in list:
    #     return list.index(search)
    # return -1


main()



