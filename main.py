# main.py
import pprint
import re

def main():
	'''main method, prompts for file from user and loads it, then 
	pass to processing'''

	OUTPUT_SUFFIX = '_abbrevs.txt'

	# text input:
	# filename = input('Please type name of a local file to process:')

	# DEBUG:
	filename = 'test1'

	# build filename 
	if filename[-4:].lower() is not OUTPUT_SUFFIX[-4:]:
		filename = filename + OUTPUT_SUFFIX[-4:]
	
	lines = list()

	with open(filename, encoding='utf-8') as text:

		for line in text:

			
			line = clean_text(line)
			print(line)
			lines.append(line)

		# TODO: rewind handle
		# rewind
		#text.seek(0)
		#
		#
    #DEBUG:
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(lines)

	write_out(filename[0:-4] + OUTPUT_SUFFIX, "this worked")


def write_out(filename, text):
	'''output a given filename with suffix to filesystem'''
	with open(filename, mode='w', encoding='utf-8') as outfile:
		outfile.write(text)

def clean_text(text):
	'''Wrangle text data, ready for processing.
	-- remove apostrophes, convert other non alphas to spaces
	and deal with whitespace.'''
	
	# remove extraneous: 
	text = text.replace("'","").strip()

	# convert some characters to spaces 

	return text

main()

	
	

