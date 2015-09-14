"""
The goal of this assignment is to classify paragraphs of
State of the Union addresses based on word counts to try
to distinguish by century. The code below will train a
Naive Bayes classifier based on word counts. It then tests
a single paragraph to see if it can classify correctly.

1. Run this code a few times. Is the category being picked
correctly often? Is this surprising? What does it seem to break
on?

2. In line 47, we check if the word is in both vocabularies.
Part of the reason for this is because we want to take the log
of the word frequency, which has some problems dealing with 0s.
If you're not familiar with logs, you can play with this function
by running

In [1]: import math
In [2]: math.log(0.1)

Try out some different numbers. Where does it break? What is
the error? Do you know of other ways we could prevent this error
besides what we do in line 47?

3. What we'd really like to do is have this check a bunch of different
test examples and tell us how often it succeeds. Can you replace the
last lines of this file with a for loop that goes through all the 
paragraphs in test_set and keeps track of how many it got right and
wrong?

4. The tokenizer we're using right now is the TreebankWordTokenizer,
which has some cool things and some not-so-cool things. Use what we
learned from the tokenizing exercise to change this tokenizer to
something you think is better. Does this improve the learning rate?

"""

# Tell python we need the natural language toolkit and 
#  a particular type of tokenizer.
import nltk
from nltk.tokenize import TreebankWordTokenizer

# Counter is a fancy dictionary. It doesn't require 
#  you to check if a symbol has been counted before.
#  You can also add and subtract Counters.
from collections import Counter

# We want to separate some of the documents as a testing
#  set, so we need a way to create random numbers
import random

# We need the log function
import math

# here's where we actually make a new tokenizer
tokenizer = TreebankWordTokenizer()

# this variable will count all the words in 18th and 19th
# century speeches
pre_1900_word_counts = Counter()

# and this one will count the rest...
post_1900_word_counts = Counter()

# create a new, empty list that will contain documents we want
#  to make predictions about.
test_set = []

def closest_century(sample_tokens):
    score = 0.0

    pre_1900_total = sum(pre_1900_word_counts.values())
    post_1900_total = sum(post_1900_word_counts.values())

    for word in sample_tokens:
        if word in pre_1900_word_counts and word in post_1900_word_counts:
            pre_score = math.log(float(pre_1900_word_counts[word]) / pre_1900_total)
            post_score = math.log(float(post_1900_word_counts[word]) / pre_1900_total)
            score += pre_score - post_score
            print "{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{}".format(pre_score, post_score, pre_score - post_score, score, word)

    if score > 0.0:
        return "pre"
    else:
        return "post"

## See http://stackoverflow.com/questions/419163/what-does-if-name-main-do
## for an explanation of this next line.
if __name__ == '__main__':

    with open("sotu_years.txt") as docs_file:
        for line in docs_file:
            ## This is a big file. To speed things up, I'll 
            ##  skip about 90% of the lines.
            if random.random() > 0.1:
                continue

            ## Break the line string everywhere there is a tab 
            ##  character, and put the resulting values into
            ##  three new variables. What would happen if there
            ##  weren't exactly two tabs in the line?
            (id, year, text) = line.split("\t")

            ## the tokenizer turns a string into a list of strings
            tokens = tokenizer.tokenize(text)

            ## declare a variable 
            doc_category = ""
            if int(year) < 1900:  ## why the int()?
                doc_category = "pre"
            else:
                doc_category = "post"

            ## We'll use 90% of the documents as training
            ## examples, and the rest for testing
            if random.random() > 0.9:
                ## the doc is in the test set, so put it
                ##  aside for now
                test_set.append( { "year": year, "category": doc_category, "tokens": tokens } )

            else:
                ## the doc is in the training set, so add
                ## it to the appropriate Counter
                if doc_category == "pre":
                    pre_1900_word_counts.update(tokens)
                else:
                    post_1900_word_counts.update(tokens)
    
    test_doc = test_set[0]
    print test_doc
    print closest_century(test_doc['tokens'])
