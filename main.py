# main.py
import re

# DEBUG
import sys
sys.stdout.buffer.write(chr(9986).encode('utf8'))


def main():
	'''main method, prompts for file from user and loads it, then 
	pass to processing'''

	OUTPUT_SUFFIX = '_abbrevs.txt'

	
	# DEBUG:
	filename = 'test1'
	# text input:
	#filename = input('Please type name of a local file to process:')


	# build filename and .txt if needed:
	if filename[-4:].lower() is not OUTPUT_SUFFIX[-4:]:
		filename = filename + OUTPUT_SUFFIX[-4:]
	
	lines = list()
	all_abbrevs = list()

	with open(filename, encoding='utf-8') as text:
		for line in text:
			
			line = clean_text(line)

			#DEBUG
			print(line, ' --- ')

			lines.append(line)
			all_abbrevs.append(find_abbrevs(line))

		# TODO: rewind handle
		# rewind
		#text.seek(0)
		#
		#
		#

    #DEBUG:
	write_out(filename[0:-4] + OUTPUT_SUFFIX, "this worked")


def write_out(filename, text):
	'''output a given filename with suffix to filesystem,
	 contain original names and order plus the chosen abbreviations.
	 (A blank given if no acceptable abbreviation).
	 All tied, best matches should be printed together.
	'''

	with open(filename, mode='w', encoding='utf-8') as outfile:
		outfile.write(text)

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
	and return as a list'''
	abbrevs = list()
	# we calculate all possible 2 and 3rd letter
	# combinations (since first index always used
	# as 1st letter of our abbreviation!).
	# We use a nested loop; discount spaces. 
	# outer loop thus runs from 2nd letter to penultimate
	# since the last letter could not act as the 2nd letter
	# of any 3-letter abbreviations.
	
	for idx_i, val_i in enumerate(line[1:-1], start=1):
		
		# skip if the value is a space (and thus falsy):
		if val_i is not ' ':
			# stem is first 2 letters of an abbreviation
			stem = line[0] + val_i

			# inner loop to find the third letter of our eventual abbreviation:
			for idx_j, val_j in enumerate(line[idx_i+1:], start=idx_i+1):
				
				if val_j is not ' ':
					abbrev = stem + val_j
					print(abbrev + ', ')
					abbrevs.append(abbrev)
		
	return abbrevs

# debug
print('---------debug----------')
main()

	
	

