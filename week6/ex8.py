"""
Name:

This week, we'll look at clustering novels based on the agglomerative
clustering method.

First we need to think about what "distance" means in this context.
We'll start with a commonly used one, Euclidean or l_2 distance.

1. Run the script. It will output the 30 closest pairs. Is this output
useful? Edit the measure_distances function and re-run until you are satisfied.

2. What are the closest non-identical pairs? Is this surprising?

3. Look at the closest pairs from different authors.
Check the original documents (use the metadata
file to find filenames). Add some comments on what you notice. Why
might these novels be "similar"?

COMMENTS HERE:

4. Try an alternative distance metric. One (absolute diff) is provided.
Are your results different?

"""
# Our novels are written in a tab-separated value file. We're going
# to use this package to read them in (also good for your comma- and
# otherwise-separated values)
import csv

# This is a dictionary with a default value (say 0, or in this case an
# empty list) that allows us to modify values for keys we haven't seen
# yet.
from collections import defaultdict

# Math. We do some.
import math


def read_novels():
    novels = []
    
    # This reads in every novel's metadata and word counts for the 10000
    # most frequent words
    with open("novel_count_file.tsv") as novelfile:
        novel_reader = csv.reader(novelfile, delimiter='\t') 
        
        # We find the titles for each of the rows, including the word list
        header_line = novel_reader.next()
        vocab = header_line[3:]

        # We read each novel into a dictionary
        for novel_data_line in novel_reader:
            title, author, year = novel_data_line[:3]
            word_count_list = [int(c) for c in novel_data_line[3:]]
            
            novel_length = sum(word_count_list)
            length_normalizer = 1.0 / novel_length
            for i in range(len(word_count_list)):
                word_count_list[i] *= length_normalizer
            
            novels.append({
                'title': title,
                'author': author,
                'year': year,
                'words': word_count_list
            })

    print "Loaded {} novels, using vocab {}".format(len(novels), len(vocab))
    return novels, vocab


def measure_distances(novels, vocab):
    novel_distances = []
    
    for novel1 in novels:
        ## Create a nice-looking view of the novel
        novel1_key = "{} / {} ({})".format(novel1['author'], novel1['title'], novel1['year'])

        for novel2 in novels:
            ## Create a nice-looking view of the other novel
            novel2_key = "{} / {} ({})".format(novel2['author'], novel2['title'], novel2['year'])

            ## Calculate the distance between the two and add this 
            ##  pair to the list.
            dist = novel_distance(novel1['words'], novel2['words'])
            novel_distances.append((novel1_key, novel2_key, dist))   
                
    return sorted(novel_distances, key=lambda pair: pair[2])

def novel_distance(novel1words, novel2words):
    # We're starting with Euclidean distance, or L2 distance:
    # for each dimension (in this case, for each word type),
    # we add the squared difference of the two values (word counts),
    # after which the final distance is the square root of this sum.
    # e.g. for 2d points (x1, y1), (x2, y2),
    # dist = sqrt((x1 - x2)^2 + (y1 - y2)^2)
    distance_squared = 0
    for count1, count2 in zip(novel1words, novel2words):
        distance_squared += (count1 - count2)**2

    # Do we actually have to do this next step?
    distance = math.sqrt(distance_squared)
    return distance

def absolute_distance(novel1words, novel2words):
    distance = 0
    for count1, count2 in zip(novel1words, novel2words):
        distance += abs(count1 - count2)

    return distance

def closest_pairs(novel_diffs, n):
    for pair in novel_diffs[:n]:
        print "{}\n\t{}\n\t{}".format(pair[2], pair[0], pair[1])


if __name__ == '__main__':
    novels, vocab = read_novels()
    novel_diffs = measure_distances(novels, vocab)
    closest_pairs(novel_diffs, 30)