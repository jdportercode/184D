import os

sdir = "/Users/jd/Documents/Courses/184D/mdw_corpus"
targets = ['men','women']
ofn = sdir + "_KWIC.tsv"


def cleanword(w,lower=True):
    if lower: 
    	w=w.lower()
    # If you want to keep numbers, change to "isalnum"
    while w and not str(w[0]).isalpha():
        w=w[1:]
    while w and not str(w[-1]).isalpha():
        w=w[:-1]
    # all of this is if you want to get rid of apostrophe s's
    # if w.endswith("'s"):
    #     w=w[:-2]
    return w

# Turn a filename into a cleaned up list of its words
def file2cleanwords(filename):
    f=open(filename)
    text=f.read()
    f.close()
    words = text.split()
    words = [cleanword(w) for w in words]
    return words

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

def get_kwic(wordlist,targetwordlist,window=5,incl_kw = False):
	kwics = []
	for n,w in enumerate(wordlist[:]):
		start = max(0,n-window)
		end = min(len(wordlist)-1,n+window)
		if w in targetwordlist:
			kwic = wordlist[start:end]
			if incl_kw == True:
				kwic = (kwic,w)
			kwics.append(kwic)
	return kwics

def dir2kwic(somedirectory,sometargetlist,window=5):
	lol = [["Filename","Keyword","Context"]]
	files = dir2files(somedirectory)
	for f in files:
		fn = os.path.join(somedirectory,f)
		text = file2cleanwords(fn)
		kwic = get_kwic(text,sometargetlist,window=window,incl_kw=True)
		for k in kwic:
			context = " ".join(k[0])
			ol = [f,k[1],context]
			lol.append(ol)
	return lol

def lol_to_file(lol,output_filename,separator="\t"):
	with open(output_filename,'w') as output_file:
		for row in lol:
			row = [str(i) for i in row]
			ostr = "\t".join(row) + "\n"
			output_file.write(ostr)
	print("Wrote the file " + output_filename)

kwics = dir2kwic(sdir,targets,window=5)
lol_to_file(kwics,ofn)
