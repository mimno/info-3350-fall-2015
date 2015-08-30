import sys

"""
This assignment is meant to test out different ways of finding the unique
tokens, or instances of words, in a document so that we can count them.

Before you start: Make sure you download the sonnets.txt file into the same
directory as your code. Open up this file in Spyder or whatever IDE you prefer.
Make sure you have NLTK installed by typing "import nltk" in the interpreter or
console and ensure that it has no error.

Problem 1: We want to start by editing this code to count words. Right
now, we're going to have a very simple definition of a word: any sequence
of characters not broken up by whitespace (spaces, tabs, new lines, etc.).
We're going to do this with the split() function, which takes a string of
characters and breaks it into pieces wherever there is whitespace. We want to
count how much each word shows up by using the dictionary word_count_dict.

We still need to fill in the code to fill in the dictionary. For any word
you haven't seen, you should set the word_count_dict for that key to be 1;
for any word in the dictionary, you want to add 1 to the value. If neither
you nor your partner have programmed, you can look at
    http://www.afterhoursprogramming.com/tutorial/Python/
for information on how to use if statements and dictionaries.

Once you get the code running, run the code to load up the sonnets.txt file.
    In [1]: word_count_dict['The']
will get the count of the word 'The'. Also check the count of 'the'. What
are they? Why are they different? Can you find how many unique words there
are in the word_count_dict?

Problem 2: It would be helpful to be able to get counts of words regardless
of upper or lower case. Search online for a Python function that will ensure
that the words are lowercased. Run the function again as above and check the
counts of 'The' and 'the' now to make sure. How many words are there now?

Problem 3: If you look in the dictionary, you'll find that there's some
assorted punctuation and cruft (for instance, 'and,'). Ultimately, we would
like to just have words. Look up the NLTK word_tokenize function, and replace
the split() function with the word_tokenize function. (You may find when you
run this that you need to download the tools - just follow the instructions
in the error message to run nltk.download() and download the punkt package
from All Packages.) Don't forget import statements!

Problem 4: We're still counting punctuation marks themselves as words.
Ultimately, we'd rather just count sequences of letters as words. To do that,
we're going to use regular expressions. Search online for the NLTK
RegexpTokenizer. Create a RegexpTokenizer that only recognizes sequences of
1 or more letters.

Extra: If you run out of things to do,
   - look up the Counter class and use that instead of the dictionary,
   - test out other regular expressions (such as one to recognize only words
   longer than two words)
   - if you split on punctuation, then contractions (like "won't") will be
   split as well. Write a regular expression that forms these into one word.
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

    with open(filename, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                # Write some code here!
                pass

    return word_count_dict


if __name__ == '__main__':
    word_count_dict = word_count('sonnets.txt')
