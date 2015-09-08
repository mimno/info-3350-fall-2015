
"""
This assignment is meant to deal with curating document vocabulary by
identifying "stop words" or words to discard. As a reminder, these assignments
are graded for participation - if you have modified the file in a way that
has relevance to what we did in class that day and/or provide interesting
answers to the problems in the comment, you will receive credit.

Before you begin:
 - Use the nltk.download() tool to get the Stopword Corpus.
 - Download the text files from the website for Shakespeare, Marlowe, and Doyle,
 and save them in the same place as this file is saved.

Problem 1: Right now, this file is set up to take the 100 most frequent
words from the corpus and treat them as useless. Try this out on the different
text samples we gave you. How do the lists compare? Are they "good" stoplists?
Does changing the number from 100 to something else help?

Problem 2: Another approach is to throw away words based on how many
documents they show up in (right now, we're treating a line in our file as a
single document). Switch to using document frequency to filter out words in
the most documents. How is it different?

Problem 3: Compare the stopwords you found to the list of stopwords from
nltk.corpus.stopwords.words('english'). How do they compare? Is one "better"?

Problem 4: This also saves a CSV file (comma-separated values) of word frequencies
across the two different files under the name "authors.csv". Open this up in your
spreadsheet viewer. How do these compare? Is there anything interesting?

Extra things:
 - what happens if you get rid of least-frequent words?
 - Some people use "stemmers" to reduce the number of different word types
 with the same format to one consistent form. For instance, a Porter stemmer
 would turn "happy", "happiness", and "happily" all into "happi". Try
applying the Porter stemmer between your tokenizer step and your word counting
step (you can look up the way to import and use the Porter stemmer from NLTK
online). How would this change your method of finding stopwords?
"""
import nltk
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter


def stopwords(filename):
    """A function that returns a dictionary with tokens as keys
    and counts of how many times each token appeared as values in
    the file with the given filename.

    Inputs:
        filename - the name of a plaintext file with a document on each line
    Outputs:
        A list of stopwords and a dictionary mapping tokens to counts.
    """
    
    # We now track the number of times a word shows up (term frequency) and
    # the number of documents with a given word in it (document frequency)
    # separately. We use a Counter, which is exactly like a dictionary except
    # - the values can only be ints
    # - any key it hasn't seen yet is assumed to already have a value of 0
    # This means we don't have to check whether we've used a key before when
    # we use the "+= 1" operation.
    term_frequency_dict = Counter()
    word_total = 0
    
    tokenizer = TreebankWordTokenizer()

    with open(filename, 'r') as f:
        for line in f:
            words = tokenizer.tokenize(line.lower())       

            # For the programmer types: there are several more efficient
            # ways to write this section using dictionaries or sets. You're
            # welcome to rewrite this part to exercise that.      
            for word in words:
                term_frequency_dict[word] += 1
                word_total += 1

    # A fun feature of Counters is that they have a built-in function that
    # gives you the n keys with the biggest values, or the "most common"
    # things being counted. We can use this to find the most common words.
    # This comes out as a list of pairs of key and value, like
    # [('foo', 10), ('bar', 7), ... , ('rare', 1)]
    stoplist_pairs = term_frequency_dict.most_common(100)
    stoplist = [word for (word, freq) in stoplist_pairs]
    
    return stoplist, term_frequency_dict, word_total


if __name__ == '__main__':
    # We run our function on two different files
    shakespath = "sonnets.txt"
    stoplist_a, term_frequency_dict_a, total_a = stopwords(shakespath)
    marlowepath = "marlowe.txt"
    stoplist_b, term_frequency_dict_b, total_b = stopwords(marlowepath)
    # This gives us the combined stoplist for the two corpora (not the
    # smartest thing - just combining the two list into one list that
    # may have some words twice)
    stoplist = stoplist_a + stoplist_b
    
    # We want to sort our list based upon how different the relative frequencies
    # are between the two authors, so we make a list of "diffs" where each entry
    # has as its first element the difference between frequencies.
    diffs = []
    for wd, afreq in term_frequency_dict_a.iteritems():
        if wd not in stoplist:
            bfreq = term_frequency_dict_b.get(wd, 0)
            diff = abs((afreq * 1.0 / total_a) - (bfreq * 1.0 / total_b))
            diffs.append((diff, wd, afreq * 1.0 / total_a, bfreq * 1.0 / total_b))
    # The sort() function automatically sorts a list in-place (i.e. the function
    # returns nothing but the diffs variable changes). It does this by default based
    # on the first element of each object, in this case the difference score.
    diffs.sort()
    # We want it most to least, not least to most.
    diffs.reverse()

    # We do some formatting fanciness to get this into a CSV format!
    with open('authors.csv', 'w') as authorfile:
        authorfile.write('Word,Shakespeare,Marlowe\n')
        for diff, wd, afreq, bfreq in diffs:
            authorfile.write('{0},{1},{2}\n'.format(wd, afreq, bfreq))
       
