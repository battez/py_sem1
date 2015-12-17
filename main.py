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


# global; stores our final abbreviations and is used by various functions
all_abbrevs = list() 

def main():
    '''main method, prompts for file from user and loads it, then 
    pass to processing'''

    # DEBUG:
    filename = 'test1'
    filename = 'trees'
    # text input:
    #filename = input('Please type name of a local file to process:')

    # build filename and .txt if needed:
    OUTPUT_SUFFIX = '_abbrevs.txt'
    if filename[-4:].lower() is not OUTPUT_SUFFIX[-4:]:
        filename = filename + OUTPUT_SUFFIX[-4:]
    
    orig_lines = list() # keep a record of original lines from file

    # Store abbrevs as keys and their values as lines they are in
    # this will help us quickly identify duplicated abbrevs
    # in other lines, and therefore to exclude them
    already = dict() 

    # a set of what we have already excluded
    excluded = set()

    # Read in the given file,
    # and generate potential abbreviations:
    with open(filename, encoding='utf-8') as text:
        
        for i, line in enumerate(text):
            
            # store the original lines in order, here, so we can 
            # look up by index later when we output:
            orig_lines.append(line)

            # remove unwanted characters etc:
            line = clean_text(line)
            
            # get the potential abbrevs for this line and update our record
            # of what we abbrevs we already have:
            (line, already, excluded) = find_abbrevs(i, line, already, excluded)

            # finally append this line to our abbrevs. 
            all_abbrevs.append(line)


        # TODO: rewind handle
        # rewind
        #text.seek(0)
        #
        #
        #

    #DEBUG
    logger.debug(excluded)

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

def find_abbrevs(line_index, line, already, excluded):
    ''' find all the possible abbreviations for a given line
    and return as a list, abbrevs.

    We calculate all possible 2 and 3rd letter
    combinations (since first index always used
    as 1st letter of our abbreviation!).

    We use a nested loop; discount spaces. 
    outer loop thus runs from 2nd letter to penultimate
    since the last letter could not act as the 2nd letter
    of any 3-letter abbreviations.'''
    result = list()
    for idx_i, val_i in enumerate(line[1:-1], start=1):
        logger.debug(line)
        # skip if the value is a space (and thus falsy):
        if val_i is not ' ':

            # stem is first two letters of an abbreviation
            stem = line[0] + val_i

            # inner loop to find the third letter of our eventual abbreviation:
            for idx_j, val_j in enumerate(line[idx_i+1:], start=idx_i+1):
                
                if val_j is not ' ':

                    # assemble abbreviation:
                    abbrev = stem + val_j
                    logger.debug(abbrev)
                    # check for duplicates of this abbrev in other lines
                    # and remove necessary if we find any:
                    if abbrev in already:

                        remove_index = already[abbrev]
                        
                        # logger.debug(line_index)
                        # logger.debug(remove_index)
                       

                        if line_index != remove_index:
                            
                            
                            # remove this abbrev. from global >> all_abbrevs:
                            purge = search_value(abbrev, all_abbrevs[remove_index])
                            
                            try:
                                logger.debug(all_abbrevs[remove_index])
                                logger.debug(purge)
                                for index in purge:
                                    all_abbrevs[remove_index].pop(index)

                                
                                # ...from already 
                                del already[abbrev]

                                # ...and add to excluded
                                excluded.add(abbrev)
                                logger.debug(excluded)

                            except ValueError:
                                pass
                            
                            # skip to next
                            continue

                    # check it is not in the excluded either:
                    if abbrev not in excluded:
                        already[abbrev] = line_index

                        # now we should append this abbreviation 
                        # as it is long enough:
                        result.append(abbrev)

    
    # TODO append a tuple with indices and score also.
    
    return (result, already, excluded)


def search_value(search, list):
    '''finds searched values in a list
    and returns a list of indices for those values'''
    result = []
    [result.append(i) for i, value in enumerate(list) if value == search]

    # we need to sort it before returning, 
    # as we might delete from the higher indices first!
    return sorted(result, reverse=True)


    # list = ['foo', 'bar', 'baz', 'foo']
    # search = 'fooh'
    # logger.debug(search_value(search, list))


    # if list.count(search):
    #     return list.index(search)
    
    # if search in list:
    #     return list.index(search)
    # return -1


main()



