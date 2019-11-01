# 184D
Code used in the course Race, Gender, and Literary Digital Humanities

The purpose of these files was primarily to demonstrate some basic Python concepts and text-mining functions, so they aren't necessarily optimized for day-to-day use. Still, they work, and the comments have pedagogical value.

**word_counter.py** has functions for reading a .txt file, performing some basic cleaning functions on the words (removing non-alphabetic characters from the ends of strings, making everything lowercase, etc.), creating a dictionary with counts for each word, and printing the results to a file (.tsv). As is, it is set up to run this on an entire directory; note that the results can get pretty unwieldy if your corpus is more than a few dozen files.

**KWIC.py** is designed to take a list of target words (e.g., ['sky', 'sea']), look through a directory of texts, and return the target words in the context, with x number of words on either side. (KWIC stands for **K**ey **W**ords **I**n **C**ontext). For instance, a window of 6 might produce output like "the brain is wider than the **sky** for put them side by side". The program takes the results and writes them to a .tsv, with columns for the target word and the file in which each KWIC was found.

**get_mdw.py** is more complicated. In short, this one takes a corpus and a metadata table that divides the corpus into two or more subcorpora. For instance, you could take few dozen 19th-century novels and divide them into "American" and "British" corpora. The program counts the words in each corpus and uses a Fisher's exact test to determine the significance of the counts relative to an "expected" even distribution across all corpora. It then writes out the significant results (p=.05 by default, but this can be changed easily) to a .tsv, with columns for the word, the corpus, the observations (how many times the word showed up), the p-value, and the observed over expected value.
