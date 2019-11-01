import os,codecs

# I like to store file and directory names at the top, in case I want to run the same program on a new folder someday 
stopfn = "/Users/jd/Documents/Courses/184D/184pydh/stopwords.txt"
sdir = "/Users/jd/Documents/Courses/184D/Corpus"
# Automatically names the output file as the directory + "wordcounts"
# Saves as a .tsv, one directory up from the sdir
ofn = sdir + "_wordcounts.tsv"

# Here we convert a string to a list of cleaned words
def string2cleanwords(somestring):
	# splits the string into a list
	words = somestring.split()
	# converts bytes to strings so we can work with them
	words = [w.decode('utf-8') for w in words]
	# this for loop cleans each word in the list "words"
	for w in words[:]:
		# this gets rid of capital letters
		w = w.lower()
		# the next two loops get rid of non-alphabetic characters on the edges of strings
		while w and not w[0].isalpha():
			w = w[1:]
		while w and not w[-1].isalpha():
			w = w[:-1]
		# this loop removes "'s"
		if w.endswith("'s"):
			w = w[:-2]
	# returns the list of cleaned words
	return words

# Opens a file of text and turns it into clean words
def file2cleanwords(somefilename):
	# Use codecs to open a text file and encode it as UTF-8
	f = codecs.open(somefilename,encoding = 'utf-8')
	# Read the file, which gives us one big string
	my_string = f.read()
	# To be good citizens, we close the file
	f.close()
	# We added this to double down on the encoding
	my_string=my_string.encode('utf-8')
	# Call the function above to turn the string into clean words
	clean_words = string2cleanwords(my_string)
	# Return our clean word list
	return clean_words

# Very basic way to turn text file into list of words
# For notes on each line in this function, see the corresponding line in file2cleanwords
def file2wordlist(somefilename):
	f = codecs.open(somefilename,encoding = 'utf-8')
	my_string = f.read()
	f.close()
	my_string = my_string.encode('utf-8')
	wordlist = my_string.split()
	return wordlist

# Turn a word list into a dictionary of type counts
def typecounter(somewordlist,somestopwordlist):
	# Make an empty dictionary
	counts = {}
	for w in somewordlist:
		# Check if words are in the stopword list
		# "continue" exits the loop entirely, so the word will not be added to counts if "continue" is triggered
		if w in somestopwordlist:
			continue
		# Check if words are in the dictionary, and set the value accordingly
		if w not in counts:
			counts[w] = 1
		else:
			counts[w] += 1
	# Give me the back the dictionary
	return counts

# This function takes a folder and gives back a list of the .txt files in it
def dir2files(somedirectory):
	files = os.listdir(somedirectory)
	# This is an on-the-fly formula that adds the directory path to the filename
	files = [os.path.join(somedirectory,f) for f in files]
	# Remove the files that don't end in ".txt"
	for i in files:
			if i[-4:] != ".txt":
				files.remove(i)
	return files

# Everything above this line is inactive; everything below it puts things into action

# The stopwords list goes outside the loop below, since it's the same every time
stopwords = file2wordlist(stopfn)

files = dir2files(sdir)

f = file2wordlist("/Users/jd/Documents/DH/Chicago/Texts/00010328.txt")
print(len(f))

# This for-loop runs a few functions on every file in the "sdir" folder
for f in files:
	# This is an optional way to see how far along you are (and make sure everything is running)
	print(f)
	words = file2cleanwords(f)
	counts = typecounter(words,stopwords)
	# We're opening a file and appending (thus 'a') our results to it
	with open(ofn,'a') as output_file:
		for key in counts:
			ostr = key + "\t" + str(counts[key]) + "\t" + f
			output_file.write(ostr)
			output_file.write("\n")