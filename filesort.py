#!/usr/bin/python
# 05/04/13
import sys, os, argparse
from re import sub, match

def main(source, dest, verbose, copy):
	filetypes = ['.avi', '.mp4', '.mkv'] # All files that will be found, edited and moved to the destination directory
	if (verbose):
		print """
Verbose mode: ON
Source directory: %s
Destination directory: %s
Searching for filetypes: (%s)

""" % (source, dest, filetypes)
	
	if (dest[-1] == '/') : dest = dest[:-1] # Remove trailing slashes
	if (source[-1] == '/') : source = source[:-1] # Remove trailing slashes

	# root is the full path
	# dirs is a list of dirs in the current dir
	# files is the list of files in current dir
	for root, dirs, files in os.walk(source):
		for file in files:
			if (file[-4:] in filetypes):
				new_filename = gen_filename(file)
				# new_filename[0] is filename
				# new_filename[1] is extension
				
				# If a similar dir has been found, change the destination ..
				find_sim_dir(new_filename[0], dest)
				# sys.exit(0)
					
				source_file = "%s/%s" % (root, file)
				dest_file = "%s/%s/%s%s"% (
					dest, new_filename[0], new_filename[0], new_filename[1])
					# The name for the destination file
				
				# If !verbose then there is no need to print
				if (verbose):
					print "Source:\t\t%s\nDestination:\t%s\n" % (source_file, dest_file)
				
				try:
					# This should happen whether -c has been used or not
					os.mkdir("%s/%s" % (dest, new_filename[0]) )
					# If -c, then copy the file, else move[rename] it
					if (copy):
						cp(source_file, dest_file)
					else:
						os.rename(source_file, dest_file)
				except:
					print "\n\nError movies file: Source:\t\t%s\nDestination:\t%s\n\n" % (
						source_file, dest_file)
					#sys.exit(1)

def gen_filename(in_name): # Generate a cleaner filename
	extension = in_name[-4:] # Save extension for later
	in_name = in_name[:-4] # Removes extension
	
	# Split the name by the first bracket, and replace all '.' with spaces
	out = in_name.split('[')[0].replace('.', ' ')
	
	# Remove common parts of names
	# The '.*' also removes everything after, since it's normally all useless,
	# but the extension has already been saved so it's not needed
	regex = '(?i)(brrip.*|xvid.*|hdrip.*|x264.*|720p.*|1080p.*|dvdrip.*|bluray.*|hdtv.*)'
	out = sub(regex, '', out)
	
	out = sub('(\ +)', ' ', out) # Change all spaces to a single space character
	out = sub('(\ +$)', '', out) # Remove trailing spaces
	out = out.title()
	
	return out, extension

def find_sim_dir(x_dir, dest_dir): # Find if there is already a directory suitable
	# Walk the destination directory and find something similar  
	word_list = x_dir.split()
	
	x = [] # Remove the word 'the' from the list and years
	for word in word_list: # x is a temporary list
		if('THE' != word.upper() and bool( match('\d{4}', word) ) == False): x.append(word)
	word_list = x
	del x # GC
	
	for root, dirs, files in os.walk(dest_dir):
		for dir in dirs:
			for word in word_list:
				if (word in dir): #
					# The file can be put in this directory
					# If it is a TV show, it also needs to find a season [WIP] 
					print "FOUND: %s\nDIR: %s\n\n" % (word, dir)
					break
					# Once a suitable directory has been found, all loops can be exited - 
					# Even returning inside the if statement
			#if 
			#print root, dir
	#print x_dir.split()

def cp(infile, outfile):
	try:
		open(outfile, "w").write(open(infile).read())
	except IOError:
		return "Error copying file\n Source: %s\tDestination: %s\n" % (infile, outfile)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-v", "--verbose", help="increase output verbosity",
		action="store_true")
	parser.add_argument("-c", "--copy", help="copy files and directories instead of moving",
		action="store_true") # WIP
	
	parser.add_argument("SOURCE", help="source directory")
	parser.add_argument("DEST", help="output directory")
	
	args = parser.parse_args()
	
	verbose = bool(args.verbose) # True if args.verbose else False
	copy 	= bool(args.copy)
	
	main(args.SOURCE, args.DEST, verbose, copy)

