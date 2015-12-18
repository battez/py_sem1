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
# scores_for_all_line_indices = list()
# global stores a parallel list for the score for each abbreviation
# in above, with the corresponding index. 
all_scores_for_abbrevs = list()

def main():
    '''Main method, prompts for file from user and loads it, then 
    passes to processing.'''
    # DEBUG:
    # filename = 'test1'
    filename = 'trees'
    # text input:
    # filename = input('Please type name of a local file to process:')

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
            
            # score this line for each of its indices, so we can lookup
            # scores_for_all_line_indices.append(score_line(line))
           

            # get the potential abbrevs for this line and update our record
            # of what abbrevs we already have:
            (line, already, excluded, line_scores) = find_abbrevs(i, line, already, excluded)

            # finally, append this line to our abbrevs.
            # and the scores for it to our other global list. 
            all_abbrevs.append(line)

            all_scores_for_abbrevs.append(line_scores)

        # TODO: rewind handle
        # rewind
        #text.seek(0)

    #
    # calculate scores here:
    # loop through all_abbrevs
    # if empty ignore
    # get min scores, if tie, append list
    # 
    # logger.debug(all_abbrevs[0:4])
    # print the original text, then its abbrevs.
    write_out(filename[0:-4] + OUTPUT_SUFFIX, orig_lines)

def write_out(filename, orig_lines):
    '''Output a given filename with suffix to filesystem,
     contain original names and order plus the chosen abbreviations.
     NB A blank given if no acceptable abbreviation. Also:
     all tied, best matches should be printed together.
    '''
    with open(filename, mode='w', encoding='utf-8') as outfile:
        for i, orig_line in enumerate(orig_lines):
            outfile.write(orig_line)
            outfile.write(' '.join(all_abbrevs[i]))
            outfile.write('\n')
            outfile.write(', '.join(map(str, all_scores_for_abbrevs[i])))
            outfile.write('\n')

    print('-----------------------------------')
    print('File has been written:', filename, ', thank you.')

def score(string):
    '''Find the score of every character in a word.
    Vowels score extra 10. 
    '''
    vowels = set('AEIOU')
    score = list()
    for idx, char in enumerate(string):
        if (idx is 0) or (char not in vowels):
            score.append(idx)
        else:
            score.append(idx + 10)
    return score

def score_line(line):
    '''Take a line and for each index calculate the scores
    for each of its indices (i.e. the chars in those indices), 
    according to the following rules:
    - index per letter, counting up from zero for word it is in
    - add 10 to any vowel chars unless they begin a word
    '''
    pieces = line.split(' ')
    scores_by_char = list()
    for idx, word in enumerate(pieces):
        # make a list of scores for each char in word:
        word_scores = score(word)
        # if there was a space we put a zero in its place too:
        if(idx < (len(pieces) - 1)):
            word_scores.append(0)
        scores_by_char += word_scores
    return scores_by_char

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
    '''Find all the possible abbreviations (and their scores) 
    for a given line and return as two lists, result and
    result_scores.

    We calculate all possible 2 and 3rd letter
    combinations (since first index always used
    as 1st letter of our abbreviation!).

    We use a nested loop; discount spaces. 
    outer loop thus runs from 2nd letter to penultimate
    since the last letter could not act as the 2nd letter
    of any 3-letter abbreviations.'''
    # first calculate the score for all chars in this line, 
    # we can then look up a score for abbrev. by indices:
    score_per_character = score_line(line)
    

    # now loop through our line and get abbreviations
    # and score them.
    result = list()
    result_scores = list()
    for idx_i, val_i in enumerate(line[1:-1], start=1):
        
        # skip if the value is a space (and thus falsy):
        if val_i is not ' ':

            # stem is first two letters of an abbreviation
            stem = line[0] + val_i

            # inner loop to find the third letter of our eventual abbreviation:
            for idx_j, val_j in enumerate(line[idx_i+1:], start=idx_i+1):
                
                if val_j is not ' ':

                    # assemble abbreviation:
                    abbrev = stem + val_j
                    
                    # check for duplicates of this abbrev in other lines
                    # and remove necessary if we find any:
                    if abbrev in already:

                        remove_index = already[abbrev]
                     
                        if line_index != remove_index:
                            
                            # remove this abbrev. from global >> all_abbrevs:
                            try:
                                for index in search_value(abbrev, all_abbrevs[remove_index]):
                                    all_abbrevs[remove_index].pop(index)
                                    all_scores_for_abbrevs[remove_index].pop(index)

                                # remove from already also
                                del already[abbrev]

                                # ...and add to excluded.
                                excluded.add(abbrev)

                            except ValueError:
                                pass
                            
                            # skip to next:
                            continue

                    # check it is not in the excluded set, either:
                    if abbrev not in excluded:

                        already[abbrev] = line_index

                        # now we should append this abbreviation 
                        # as it is valid and long enough:
                        result.append(abbrev)
                        # sum its characters' scores and append:
                        abbrev_score = score_per_character[idx_i] + \
                        score_per_character[idx_j]

                        result_scores.append(abbrev_score)

    # return the result with updated abbrevs, and also 
    # updated versions of already dict and excluded set.
    # also append a list with corresponding scores also.
    return (result, already, excluded, result_scores)

def search_value(search, list):
    '''Find searched values in a list
    and return a list of indices for those values'''
    result = []
    [result.append(i) for i, value in enumerate(list) if value == search]

    # we need to sort it before returning, as we 
    # want to delete from the higher indices first.
    return sorted(result, reverse=True)

main()



