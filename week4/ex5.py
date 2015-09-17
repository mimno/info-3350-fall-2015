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
from collections import defaultdict

# We want to separate some of the documents as a testing
#  set, so we need a way to create random numbers
import random

# We need the log function
import math

# We also want a standard deviation function
import numpy

# Finally, we want to plot stuff
import matplotlib.pyplot as plt

# here's where we actually make a new tokenizer
tokenizer = TreebankWordTokenizer()


# This is how we pick how many years are in each category
epoch_length = 25

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
            
            # This is a little trick to make every year within an epoch
            # into the first year of that epoch (a case where integer
            # arithmetic comes in handy)
            # e.g. 1777 / 25 = 71, 71 * 25 = 1775
            doc_category = (int(year) / epoch_length) * epoch_length

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
# Our process is going to be to look at each category and compute one score
# for it. If it is 
def closest_century(sample_tokens, category_word_counts):
    # Python lets us use something like infinity as a default for
    # cases like this when we need a number lower than any possible number.
    best_score = float("-inf")
    # We're also using the first year (as an int) as the name of each category
    # now, so we're using 0 as a starting best category that is recognizably
    # not a valid response so we can tell if things broke.
    best_category = 0

    for category in category_word_counts.keys():
        # We're finding the category sum in this loop so we only have
        # one to track at a time.
        total = sum(category_word_counts[category].values())

        score = 0.0
        for word in sample_tokens:
            # This is one approach for dealing with words we haven't seen: 
            # we can "smooth" the values by assuming some tiny possibility
            # of a word appearing regardless of if we've seen it or not. In
            # this case, we're saying that every possible word in this corpus
            # showed up 0.1 times extra in each category. This makes the log
            # positive and makes sure we can compare rare words that might be
            # a really strong signal.
            score += math.log((0.1 + float(category_word_counts[category][word])) / total)
        # The score will be a negative number, but a *less* negative
        # number for the most likely category.
        if score > best_score:
            best_score = score
            best_category = category
        
def train_and_test_classifier(test_set, train_set):
    # this variable will keep track of word counts for
    # each period of time starting with the year we give it.
    # A defaultdict is a generalization of a Counter for
    # whatever default value you might have. In this case,
    # any key we haven't used yet has a value that's an empty Counter.
    # So, we'll end up with one counter for each category that will
    # keep track of the token counts for that category.
    category_word_counts = defaultdict(Counter)

    # This one is going to keep track of our guesses:
    # confusion_matrix[cata][catb] will be the count of how many
    # times the actual category was cata and our prediction was catb
    # e.g. confusion_matrix[1825][1850] would be the count of times
    # something in 1825-49 was guessed as being in 1850-74.
    confusion_matrix = defaultdict(Counter)

    # We add the training data to our categories
    for doc in train_set:
        category_word_counts[doc['category']].update(doc['tokens'])
    
    # We count how many times we classify correctly
    for test_doc in test_set:
        prediction = closest_century(test_doc['tokens'], category_word_counts)
        confusion_matrix[test_doc["category"]][prediction] += 1

    return confusion_matrix

## See http://stackoverflow.com/questions/419163/what-does-if-name-main-do
## for an explanation of this next line.
if __name__ == '__main__':
    
    # We're going to keep track of a running confusion matrix
    total_confusion_matrix = defaultdict(Counter)

    # For each train/test split, we generate a new confusion matrix
    # and use nice Counter addition to add in the new values to the existing
    # ones.
    for train_set, test_set in train_test_splits():
        new_confusion_matrix = train_and_test_classifier(train_set, test_set)
        for actual_cat, prediction_counter in new_confusion_matrix.items():
            total_confusion_matrix[actual_cat] += prediction_counter
    
    # We now want to plot our confusion matrix. To do this, we first
    # want to turn this from a dictionary of dictionaries to an array
    # of arrays in order by category.

    # Our list of categories in order (i.e. [1775, 1800, 1825, ..., 2000])
    categories = sorted(total_confusion_matrix.keys())
    confusion_matrix_array = []
    for cat1 in categories:
        row = [total_confusion_matrix[cat1][cat2] for cat2 in categories]
        confusion_matrix_array.append(row)

    print confusion_matrix_array

    # We're going to make a figure with a confusion matrix as a
    # plot. We want it to be square, or to have an 'equal' aspect
    # ratio.
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    cax = ax.matshow(confusion_matrix_array)
    fig.colorbar(cax)
    ax.set_xticklabels(categories)
    ax.set_yticklabels(categories)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.show()
