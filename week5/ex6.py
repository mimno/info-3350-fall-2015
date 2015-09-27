"""
Name:

The goal of this exercise is to see some of the properties of ensembles
of classifiers. Each individual classifier will not be very good, but 
when we combine them we get some interesting properties.

1. Familiarize yourself with the code. Look through the "def" statements
to find the functions. Look through the "main" section at the bottom of 
this document to see how they fit together.

2. Run the code. The original setting trains 10 classifiers, each on a
randomly selected 10% subsample of the training documents. What accuracy
do you get? Run this a few times, and compare with neighbors, to get a
sense of the variability of this number.

3. What setting would replicate the "real" classifier? In other words,
how would you use this code to train a single classifier on all the training
data? What accuracy do you get with that setting? As before, run it a 
few times to see variability.

4. Try various settings of number of classifiers and proportion of 
training data. What is the effect of reducing the training data on a 
single classifier? Does adding more classifiers improve accuracy?

5. Be naughty! Test on the training data. What accuracy do you get from
an ensemble of not-all-the-training-data classifiers? What about a 
single classifier from all the training data? Do you see a difference? 
Why or why not?
"""

# Tell python we need the natural language toolkit and 
#  a particular type of tokenizer.
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

# Finally, we want to plot stuff
import matplotlib.pyplot as plt

# here's where we actually make a new tokenizer
tokenizer = TreebankWordTokenizer()


# This is how we pick how many years are in each category
epoch_length = 25

## Read
def read_documents(proportion_to_ignore):
    # We're going to read in the lines once so we can do the splitting
    # into sets one or more times after the file is closed.
    doc_dicts = []
    with open("sotu_years.txt") as docs_file:
        for line in docs_file:
            ## This is a big file. To speed things up, I'll 
            ##  skip about 80% of the lines.
            if random.random() < proportion_to_ignore:
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

    return doc_dicts

## Randomly divide a list into two lists
def split_documents(doc_dicts, training_proportion):

    train_list = []
    test_list = []

    for doc_dict in doc_dicts:            
        if random.random() > training_proportion:
            ## the doc is in the test set, so put it
            ##  aside for now
            test_list.append(doc_dict)
        else:
            train_list.append(doc_dict)
                
    return (train_list, test_list)
    

## Create a new, smaller training set. 
## Randomly drop the specified proportion of documents
def subsample(original_list, proportion_to_drop):

    subsampled_list = []

    for doc in original_list:
        if random.random() > proportion_to_drop:
            subsampled_list.append(doc)

    return subsampled_list

def train_classifier(train_list):
    # this variable will keep track of word counts for
    # each period of time starting with the year we give it.
    # A defaultdict is a generalization of a Counter for
    # whatever default value you might have. In this case,
    # any key we haven't used yet has a value that's an empty Counter.
    # So, we'll end up with one counter for each category that will
    # keep track of the token counts for that category.
    category_word_counts = defaultdict(Counter)

    # We add the training data to our categories
    for doc in train_list:
        category_word_counts[doc['category']].update(doc['tokens'])

    return category_word_counts

## This function creates a specified number of classifiers, each
##  trained on a subset of the training documents.
def create_ensemble(original_training_list, proportion_to_drop, ensemble_size):

    classifiers = []

    for i in range(0, ensemble_size):
        subsampled_training_list = subsample(original_training_list, proportion_to_drop)
        classifiers.append( train_classifier(subsampled_training_list) )

    return classifiers

# Our function for checking which epoch is closer. Note that now, we need
# to pass through the word counts from the training set we have.
# Our process is going to be to look at each category and compute one score
# for it. If it is the best score so far, we'll pick that as the best category
# so far. 
def closest_epoch(sample_tokens, category_word_counts):
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
        nwords = len(category_word_counts[category])

        score = 0.0

        for word in sample_tokens:
            # This is one approach for dealing with words we haven't seen: 
            # we can "smooth" the values by assuming some tiny possibility
            # of a word appearing regardless of if we've seen it or not. In
            # this case, we're saying that every possible word in this corpus
            # showed up 0.1 times extra in each category. This makes the log
            # positive and makes sure we can compare rare words that might be
            # a really strong signal.
            score += math.log((0.001 + float(category_word_counts[category][word])) / (total + 0.001*nwords))
        # The score will be a negative number, but a *less* negative
        # number for the most likely category.
        if score > best_score:
            best_score = score
            best_category = category
    return best_category
        
## We expect each of our classifiers to be fairly weak. But can 
##  they work together? This function uses a simple majority
##  voting rule to combine multiple classifiers and produce
##  a single prediction.
def get_majority_prediction(test_doc, classifiers):

    votes = Counter()

    for category_word_counts in classifiers:
        prediction = closest_epoch(test_doc['tokens'], category_word_counts)
        votes[prediction] += 1
        
    ## Which epoch had the most votes?
    max_epoch = ""
    max_count = 0

    for epoch in votes.keys():
        if votes[epoch] > max_count:
            max_epoch = epoch
            max_count = votes[epoch]

    return max_epoch

def evaluate(classifiers, test_list):
    
    # This dictionary of Counters is going to keep track of our guesses:
    # confusion_matrix[cata][catb] will be the count of how many
    # times the actual category was cata and our prediction was catb
    # e.g. confusion_matrix[1825][1850] would be the count of times
    # something in 1825-49 was guessed as being in 1850-74.
    confusion_matrix = defaultdict(Counter)
    correct_predictions = 0.0
    
    # We count how many times we classify correctly
    for test_doc in test_list:
        prediction = get_majority_prediction(test_doc, classifiers)
        if prediction == test_doc["category"]:
            correct_predictions += 1
        confusion_matrix[test_doc["category"]][prediction] += 1

    print "accuracy: {}%".format(100 * correct_predictions / len(test_list))
    return confusion_matrix

## See http://stackoverflow.com/questions/419163/what-does-if-name-main-do
## for an explanation of this next line.
if __name__ == '__main__':
    
    ## Read the file, dropping 80% of documents,
    ##  so that we can try several experiments quickly.
    all_docs = read_documents(0.8)

    ## get a test/train split
    (train_list, test_list) = split_documents(all_docs, 0.8)

    ## Create this many classifiers, each trained on a subset
    ##  of the full training set.
    num_classifiers = 10
    proportion_of_training_to_drop = 0.9
    classifiers = create_ensemble(train_list,
                                  proportion_of_training_to_drop,
                                  num_classifiers)
                                  
    ## Get the confusion matrix, but this time use the majority
    ##  vote of the classifiers on each testing document                            
    confusion_matrix = evaluate(classifiers, test_list)
    
    # We now want to plot our confusion matrix. To do this, we first
    # want to turn this from a dictionary of dictionaries to an array
    # of arrays in order by category.

    # Our list of categories in order (i.e. [1775, 1800, 1825, ..., 2000])
    categories = sorted(confusion_matrix.keys())
    confusion_matrix_array = []
    for cat1 in categories:
        row = [total_confusion_matrix[cat1][cat2] for cat2 in categories]
        confusion_matrix_array.append(row)

    #print confusion_matrix_array

    # We're going to make a figure with a confusion matrix as a
    # plot. We want it to be square, or to have an 'equal' aspect
    # ratio.
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    cax = ax.matshow(confusion_matrix_array)
    fig.colorbar(cax)
    ax.set_xticklabels([''] + categories)
    ax.set_yticklabels([''] + categories)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.show()
