"""
Name:

The goal of this assignment is to test a classifier on State of
the Union paragraphs to see how well it is classifying.

1. Look at how the testing is done right now in test_train_splits().
What is this method called?
Answer:

2. Run this a few times. What accuracy do you get?

3. Try out some of the other techniques:
   - random subsampling,
   - leave-one-out cross validation,
   - five-fold cross validation...
   Which of these are easy to write? Which seem most precise?
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

# We also want a standard deviation function
import numpy

# here's where we actually make a new tokenizer
tokenizer = TreebankWordTokenizer()


# This function returns a list of pairs of a test set and a training set.
# This way we can try out a bunch of different testing and training splits.
def train_test_splits():
    # We're going to read in the lines once so we can do the splitting
    # into sets one or more times after the file is closed.
    doc_dicts = []
    with open("sotu_years.txt") as docs_file:
        for line in docs_file:
            ## This is a big file. To speed things up, I'll 
            ##  skip about 80% of the lines.
            if random.random() > 0.2:
                continue

            ## Break the line string everywhere there is a tab 
            ##  character, and put the resulting values into
            ##  three new variables. What would happen if there
            ##  weren't exactly two tabs in the line?
            (id, year, text) = line.split("\t")

            ## the tokenizer turns a string into a list of strings
            tokens = tokenizer.tokenize(text)
            
            # find the category
            if int(year) < 1900:  ## why the int()?
                doc_category = "pre"
            else:
                doc_category = "post"

            ## We'll use 80% of the documents as training
            ## examples, and the rest for testing
            doc_dict = { "year": year, "category": doc_category, "tokens": tokens }
            doc_dicts.append(doc_dict)

    # Where the magic happens. Eventually, we'll want to make more
    # than one (training set, test set) pair. I recommend a for loop.
    train_set = []
    test_set = []
    for doc_dict in doc_dicts:            
        if random.random() > 0.8:
            ## the doc is in the test set, so put it
            ##  aside for now
            test_set.append(doc_dict)
        else:
            train_set.append(doc_dict)
                
    return [(train_set, test_set)]
    

# Our function for checking which century is closer. Note that now, we need
# to pass through the word counts from the training set we have.
def closest_century(sample_tokens, pre_1900_word_counts, post_1900_word_counts):
    score = 0.0

    pre_1900_total = sum(pre_1900_word_counts.values())
    post_1900_total = sum(post_1900_word_counts.values())

    for word in sample_tokens:
        if word in pre_1900_word_counts and word in post_1900_word_counts:
            pre_score = math.log(float(pre_1900_word_counts[word]) / pre_1900_total)
            post_score = math.log(float(post_1900_word_counts[word]) / post_1900_total)
            score += pre_score - post_score

    if score > 0.0:
        return "pre"
    else:
        return "post"
        
        
def train_and_test_classifier(test_set, train_set):
    # this variable will count all the words in 18th and 19th
    # century speeches
    pre_1900_word_counts = Counter()
    
    # and this one will count the rest...
    post_1900_word_counts = Counter()
    
    for doc in train_set:
        if doc['category'] == "pre":
            pre_1900_word_counts.update(doc['tokens'])
        else:
            post_1900_word_counts.update(doc['tokens'])
    
    # We cound how many times we classify correctly
    successes = 0.0
    for test_doc in test_set:
        if closest_century(
                test_doc['tokens'],
                pre_1900_word_counts,
                post_1900_word_counts) == test_doc["category"]:
            successes += 1

    # Is this line correct?
    success_rate = successes / len(test_set)
    return success_rate
                
                    
## See http://stackoverflow.com/questions/419163/what-does-if-name-main-do
## for an explanation of this next line.
if __name__ == '__main__':
    success_rates = []                    
    for train_set, test_set in train_test_splits():
        success_rates.append(train_and_test_classifier(train_set, test_set))
    
    # Compute some statistics over the trials to get our 
    mean = numpy.average(success_rates)
    stderr = numpy.std(success_rates) / math.sqrt(len(success_rates))
    print "Average success rate: {0:.2f} +/- {1:.2f}".format(mean, stderr)
