# main.py

def main():
	'''main method, prompts for file from user and loads it, then 
	pass to processing'''

	OUTPUT_SUFFIX = '_abbrevs.txt'

	filename = "trees"

	# build filename 
	if filename[-4:].lower() is not OUTPUT_SUFFIX[-4:]:
		filename = filename + OUTPUT_SUFFIX[-4:]
  
	with open(filename, encoding = 'utf-8') as text:
		text.read()

		# TODO: rewind handle
		# rewind
		#text.seek(0)
		#
    


main()

	
	

