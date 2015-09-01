import nltk
from nltk.tokenize import RegexpTokenizer

"""
This assignment is meant to deal with text encodings.

Before you begin: Download the Polish unicode sample text using the
nltk.download() window and the Corpora tab. You'll need this to get the file
to run the code below successfully.

Problem 1: Run this file. Look at the keys in the output dictionary
word_count_dict. What do you notice? Why do you think this is? What kind of
content do you think this file has?

Problem 2: This file happens to have the encoding latin2. We can use the
codecs module to allow us to open the file. Look up codecs.open examples and
replace the open(filename, 'r') with a codecs.open command for latin2. What
changes? Is the number of keys the same? Why?

Problem 3: We'd like to write this text out in a more conventional encoding.
In this case, we'd prefer Unicode. Open a file using the codecs file open
command, this time replacing the 'r' with 'w' (for 'write' instead of 'read')
and specifying the utf-8 encoding (a specific type of Unicode encoding).
Write code at the end of this function to write out the list of words in the
file. This requires the file object's write function - feel free to look up
examples of it, and make sure to add a '\n' to end your lines. You probably
will also want the dictionary keys() function. Choose whatever name you want
for the new file.

Problem 4: Change the last file to call the word_count function on the
new file, and rewrite the code to handle the UTF-8 encoded text. Check
that it's reading in correctly. This will be useful if you ever need to
convert a variety of different types of texts to the same format - especially
if you want to tokenize or otherwise preprocess as you do it.

Problem 5: Try to read in some other complex UTF-8 text like the Urdu file and
Tweets file from the website. What happens if you read them in with the wrong
encoding?

Extra things:
  - print the words AND their counts as a CSV (comma-separated values file).
  You can look up what this format looks like online: basically, it corresponds
  to a way of representing spreadsheet data where commas represent split columns
  and new lines split rows. You can do this using the csv module or with just
  clever "text munging" (or adding bits of strings together with +)
  - sort the words in the output file by frequency and by alphabetical order
  - play with some of the different tokenizers from Monday. Is the starting
  one good, or are there better options? How about with the urdu-sample.txt file
  from the website?
"""

def word_count(filename):
    """A function that returns a dictionary with tokens as keys
    and counts of how many times each token appeared as values in
    the file with the given filename.

    Inputs:
        filename - the name of a plaintext file
    Outputs:
        A dictionary mapping tokens to counts.
    """

    word_count_dict = {}
    tokenizer = RegexpTokenizer('\w+')

    with open(filename, 'r') as f:
        for line in f:
            words = tokenizer.tokenize(line.lower())
            for word in words:
                if word not in word_count_dict:
                    word_count_dict[word] = 1
                else:
                    word_count_dict[word] += 1

    return word_count_dict


if __name__ == '__main__':
    path = nltk.data.find('corpora/unicode_samples/polish-lat2.txt')
    word_count_dict = word_count(path)
