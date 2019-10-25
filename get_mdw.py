#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,codecs,scipy.stats

# Give the full path to your metadata table here (on a Mac, cmd-opt-c while highlighting the file in Finder)
metadata = "/Users/jd/Documents/DH/Ellison/SmallerCorpusMetadata.txt"
# Give the full path to the folder containing your corpus
sdir = "/Users/jd/Documents/DH/Ellison/SmallerCorpus"
# The results will write as a file one directory up, named [YourFolder]_mdw.csv
ofn = sdir + "_mdw.tsv"

'''
x 1. Make metadata table (metatable)
x 2. Make count dictionaries for the individual subcorpora (corp_dict)
x 3. Get the overall word counts for the subcorpora (wcd)
x 4. Get the word counts for the full corpus (counts)
x 5. Convert those counts to rates (rates)
x 6. Turn the subcorpus dictionaries into a tdm (tdm)
x 7. Melt the tdm (melted_tdm)
x 8. Get the mdw data and add to tdm
x 9. Write to a file
x 10. Combine steps
'''

# Turn a spreadsheet into a list of lists
def sheet2lol(fn,separator=","):
	f=codecs.open(fn,encoding="utf-8-sig")
	text=f.read()
	f.close()
	lines = text.splitlines()
	lol = []
	for l in lines:
		l = l.split(separator)
		lol.append(l)
	return lol

# Turn a directory into a list of its text files
# Your files must all end with .txt
def dir2files(somedirectory,path=False):
	if path == False:
		files = os.listdir(somedirectory)
	else:
		files = os.listdir(somedirectory)
		files = [os.path.join(somedirectory,f) for f in files]
	for i in files[:]:
			if not i.endswith(".txt"):
				files.remove(i)
	return files

# Clean words; you may wish to adjust the parameters here
# Usually want to make lowercase, but might not with names
def cleanword(w,lower=True):
    if lower: 
    	w=w.lower()
    # If you want to keep numbers, change to "isalnum"
    while w and not str(w[0]).isalpha():
        w=w[1:]
    while w and not str(w[-1]).isalpha():
        w=w[:-1]
    # all of this is if you want to get rid of apostrophe s's
    if w.endswith("'s"):
        w=w[:-2]
        #w=w+"s"
    return w

# Turn a filename into a cleaned up list of its words
def file2cleanwords(filename):
    f=open(filename)
    text=f.read()
    f.close()
    # Get rid of curly quotes and apostrophes
    text = text.replace('\u2019',"'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"').replace("‘","'").replace("’","'").replace('“','"').replace("”",'"').replace('\xa0', ' ')
    words = text.split()
    words = [cleanword(w) for w in words]
    return words

# Get the unique values in a spreadsheet column
# (Actually a list of lists now, but same idea)
def unique_col_values(somedf,col_num,header=True):
	values = []
	if header == True:
		somedf = somedf[1:]
	for row in somedf:
		v = row[col_num]
		if v not in values:
			values.append(v)
	return values

# Turn your corpora into wordcount dictionaries
# This will be a dictionary of dictionaries
# For this to work as is, your metadata table must have filenames but not path names
def makecorpusdicts(somedir,metatable,meta_col_num,fn_col_num):
	corp_dict = {}
	files = dir2files(somedir)
	corpora = unique_col_values(metatable,meta_col_num)
	for c in corpora:
		corp_dict[c] = {}
	for row in metatable[1:]:
		f = row[fn_col_num].strip('"')
		fn = os.path.join(somedir,f)
		words = file2cleanwords(fn)
		cd = str(row[meta_col_num])
		for w in words:
			if w in corp_dict[cd]:
				corp_dict[cd][w] += 1
			else:
				corp_dict[cd][w] = 1
	return corp_dict

# Get word counts for your copora from the "makecorpusdicts" output
# This would work for any such dictionary of dictionaries
def get_wcd(corp_dict):
	wcd = {}
	for d in corp_dict:
		tempd = dict(corp_dict[d])
		wcd[d] = sum(tempd.values())
	return wcd

# Turn a directory of text files into an overall dictionary of word counts
def dir2counts(somedir):
	counts = {}
	files = dir2files(somedir,path=True)
	for f in files:
		words = file2cleanwords(f)
		for w in words:
			if w in counts:
				counts[w] += 1
			else:
				counts[w] = 1
	return counts

# For MDW, we want word rates
# I.e. how often a word appears given the word count
# This converts a counts dictionary to a rates dictionary
def counts2rates(somecountdict):
	rates = dict(somecountdict)
	total = sum(somecountdict.values())
	for key in rates:
		rates[key] = float(rates[key])/total
	return rates

# Make your dictionaries a term document matrix
# This gives you a good way to A) produce writable output
# And B), go through and get MDW later on
# min_obs refers to total observations across all corpora
def dicts2tdm(dictofcountdicts,min_obs=0,no_numbers=False):
	# I'm removing any corpus that had no actual values found; might not want to do this
	# for d in dictofcountdicts:
	# 	if sum(dictofcountdicts[d].values()) == 0:
	# 		del dictofcountdicts[d]
	tdm = [['token_']+list(dictofcountdicts.keys())]
	all_words = []
	for d in dictofcountdicts:
		for w in list(dictofcountdicts[d].keys()):
			if w not in all_words:
				all_words.append(w)
	for w in all_words:
		row=[w]
		for col in tdm[0][1:]:
			if w in dictofcountdicts[col]:
				row.append(dictofcountdicts[col][w])
			else:
				row.append(0)
		tdm.append(row)
	if no_numbers == True:
		for row in tdm[1:]:
			if is_number(row[0]):
				tdm.remove(row)
	for row in tdm[1:]:
		if sum(row[1:]) < min_obs:
			tdm.remove(row)
	return tdm

# 'Melts' the tdm
# Which means columns are types of data instead of particular instances of that type
# E.g. instead of columns for "Western" and "Sci-Fi" you'd have "Genre" and list the two types under it for each word
def tdm_melter(sometdm):
	old_headers = sometdm[0]
	melt = [['token_','Corpus','Observations']]
	for row in sometdm[1:]:
		for n,col in enumerate(row[1:],1):
			ol = [row[0],old_headers[n],row[n]]
			melt.append(ol)
	return melt

# Do a Fishers exact test, mdw style
def get_fishers(melted_tdm_row,wcd,word_rates,obs_exp=False,alternative="greater"):
	corpus = melted_tdm_row[1]
	wc = wcd[corpus]
	word = melted_tdm_row[0]
	rate = word_rates[word]
	a = melted_tdm_row[2]
	b = wc-a
	c = round(rate*wc)
	d = wc-c
	p = scipy.stats.fisher_exact([[a,b],[c,d]],alternative=alternative)[1]
	if obs_exp == True:
		if c != 0:
			oe = a/c
		else:
			oe = "Inf"
		p = (p,oe)
	return p

# Get the actual mdw data and append to the tdm
def add_mdw(melted_tdm,wcd,word_rates,obs_exp=True,alpha=.05,alternative="greater"):
	melted_tdm[0].extend(['p_value','Obs/Exp'])
	for row in melted_tdm[1:]:
		duple = get_fishers(row,wcd,word_rates,obs_exp=obs_exp,alternative=alternative)
		p = duple[0]
		if p >= alpha:
			melted_tdm.remove(row)
		else:
			row.extend([p,duple[1]])
	return melted_tdm

# Turns our list of lists into a spreadsheet, located wherever you put it
# I recommend using tab separation, but commas are sometimes preferable
def lol_to_file(lol,output_filename,separator="\t"):
	with open(output_filename,'w') as output_file:
		for row in lol:
			row = [str(i) for i in row]
			ostr = "\t".join(row) + "\n"
			output_file.write(ostr)
	print("Wrote the file " + output_filename)

# Combine all the functions above to get MDW from a metadata table and a corpus
# If there's an equals sign in any of the inputs, you don't have to write anything unless you want to change the default
# Otherwise, you have to write something
def get_mdw(metadata_table_fn,metadata_column_num,filename_col_num,source_directory,output_filename,metadata_table_separator=",",keep_uppercase=False,minimum_observations=0,fishers_alternative="greater",alpha=.05,output_filename_separator="\t"):
	print("Reading metadata table...")
	metatable = sheet2lol(metadata_table_fn,separator=metadata_table_separator)
	print("Making a wordcount dictionary for each subcorpus...")
	corp_dict = makecorpusdicts(source_directory,metatable,meta_col_num=metadata_column_num,fn_col_num=filename_col_num)
	print("Getting total word counts for your subcorpora...")
	wcd = get_wcd(corp_dict)
	print("Getting word counts for the full corpus...")
	counts = dir2counts(source_directory)
	print("Coverting those counts to rates...")
	rates = counts2rates(counts)
	print("Making a tdm out of the individual corpus counts...")
	tdm = dicts2tdm(corp_dict,min_obs=minimum_observations)
	print("Melting the tdm...")
	melted_tdm = tdm_melter(tdm)
	print("Getting mdw data...")
	mdw = add_mdw(melted_tdm,wcd,rates,alpha=alpha,alternative=fishers_alternative)
	print("Writing data to file...")
	lol_to_file(mdw,output_filename)

# Don't forget, python starts counting a list at zero
get_mdw(metadata,metadata_column_num=1,filename_col_num=0,source_directory=sdir,output_filename=ofn,metadata_table_separator="\t",minimum_observations=50)

