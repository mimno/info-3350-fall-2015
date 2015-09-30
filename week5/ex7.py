"""
Name:

A decision tree is a classifier that splits a corpus of training
examples based on a sequence of simple if/else questions.

We can train a decision tree by finding the word that best "splits"
the data set, and then recursively find the best split on each of
the resulting sub-training sets.

Since we're all tired of US history, we're now working with Greek 
history. Can we distinguish English translations of Thucydides and
Herodotus?

1. Run the script. What is the most distinguishing feature? Look
at the file thuc_herod.txt and see if you can understand why.

2. Our criterion for a split is "entropy", which can be thought of 
as a measure of unpredictability. The entropy() function takes 
a Counter and returns the entropy of probability distribution that
is proportional to the counts. Try different values of this function.

3. Back to Herodotus and Thucydides: can you filter out the feature
that was the most salient in #1 above? What does the decision tree
look like now?

4. We're passing in a list of "splittable" words. By default this
list is the words that occur more than 100 times in the training list.
How would we count the number of paragraphs each word appears (at 
least once) in, rather than the total number of occurrences?

5. What if we subsample this list? Do you get different trees each time?

"""

# Tell python we need the natural language toolkit and 
#  a particular type of tokenizer.
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

vocab = Counter()

## Read
def read_documents(proportion_to_ignore):
    # We're going to read in the lines once so we can do the splitting
    # into sets one or more times after the file is closed.
    doc_dicts = []
    with open("thuc_herod.txt") as docs_file:
        for line in docs_file:
            ## This is a big file. To speed things up, I'll 
            ##  skip about 80% of the lines.
            if random.random() < proportion_to_ignore:
                continue
            
            ## Break the line string everywhere there is a tab 
            ##  character, and put the resulting values into
            ##  three new variables. What would happen if there
            ##  weren't exactly two tabs in the line?
            (id, author, text) = line.split("\t")

            ## the tokenizer turns a string into a list of strings
            tokens = tokenizer.tokenize(text)
            
            ## We'll use 80% of the documents as training
            ## examples, and the rest for testing
            doc_dict = { "category": author, "tokens": tokens }
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
    

## Create a new, smaller list. 
## Randomly drop the specified proportion of elements.
def subsample(original_list, proportion_to_drop):

    subsampled_list = []

    for element in original_list:
        if random.random() > proportion_to_drop:
            subsampled_list.append(element)

    return subsampled_list

def entropy(counter, total=None):
    if total == None:
        total = sum(counter.values())
    if total == 0:
        return None
    result = total * math.log(total)
    for n in counter.values():
        result -= n * math.log(n)
    return result / total

def split_score(train_list, word):
    with_counter = Counter()
    without_counter = Counter()

    for doc in train_list:
        if word in doc["tokens"]:
            with_counter[ doc["category"] ] += 1
        else:
            without_counter[ doc["category"] ] += 1
            
    with_total = sum(with_counter.values())
    without_total = sum(without_counter.values())
    
    if with_total == 0 or without_total == 0:
        return None

    return ( with_total, entropy(with_counter, with_total),
             without_total, entropy(without_counter, without_total), word )

def get_best_split(words, train_list, depth, max_depth):
    word_scores = []
    for word in words:
        split_stats = split_score(train_list, word)
        if not split_stats == None:
            word_scores.append(split_stats)
                
    if len(word_scores) == 0:
        return

    best_split = sorted(word_scores, key=lambda w: w[0] * w[1] + w[2] * w[3])[0]
    score = best_split[0] * best_split[1] + best_split[2] * best_split[3]
    print "{}{}\t{:.3f}\t{}\t{:.3f}\t{}".format(" " * depth, best_split[0], best_split[1], best_split[2], best_split[3], best_split[4])

    if depth < max_depth and score > 0.0:
        get_best_split(words, [doc for doc in train_list if best_split[4] in doc["tokens"]], depth + 1, max_depth)
        get_best_split(words, [doc for doc in train_list if not best_split[4] in doc["tokens"]], depth + 1, max_depth)

## See http://stackoverflow.com/questions/419163/what-does-if-name-main-do
## for an explanation of this next line.
if __name__ == '__main__':
    
    ## Read the file, dropping 80% of documents,
    ##  so that we can try several experiments quickly.
    all_docs = read_documents(0.0)

    ## get a test/train split
    (train_list, test_list) = split_documents(all_docs, 0.8)

    for doc in train_list:
        vocab.update(doc["tokens"])

    frequent_words = [word for word in vocab.keys() if vocab[word] > 100]
    
    get_best_split(frequent_words, train_list, 0, 3)
