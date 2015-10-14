"""
Name:



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

# We will initialize randomly
import random

# Tools for lists of numbers
import numpy

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
            
            ## everything from index 3 on is a string
            ##  representing a word count
            count_strings = novel_data_line[3:]
            word_count_list = numpy.zeros(len(count_strings))

            for i in range(0, len(count_strings)):
                word_count_list[i] = float(count_strings[ i ])

            novel_length = numpy.sum(word_count_list)
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

def random_clusters(novels, num_clusters):
    clusters = []

    for i in range(0, num_clusters):
        ## create an empty list for cluster i
        clusters.append([])

    for novel in novels:
        ## Grab a random cluster list
        cluster = random.choice( clusters )
        cluster.append( novel )

    return clusters

def cluster_novels(novels, vocab, clusters):

    ## Find the mean of each cluster
    cluster_means = []
    for cluster in clusters:
        if len(cluster) == 0:
            continue

        mean_counts = numpy.zeros( len(vocab) )
        for novel in cluster:
            mean_counts += novel['words']
        mean_counts /= len(cluster)

        cluster_means.append(mean_counts)

    ## Clear the current clusters
    for i in range(0, len(clusters)):
        clusters[i] = []

    total_distance = 0
    for novel in novels:
        distances_to_clusters = numpy.zeros( len(clusters) )
        for cluster_id in range(0, len(clusters) ):
            distances_to_clusters[ cluster_id ] = novel_distance( cluster_means[ cluster_id ], novel['words'] )

        best_cluster = numpy.argmin( distances_to_clusters )
        clusters[ best_cluster ].append(novel)

        total_distance += distances_to_clusters[ best_cluster ]

    return total_distance

def novel_distance(novel1words, novel2words):
    # We're starting with Euclidean distance, or L2 distance:
    # for each dimension (in this case, for each word type),
    # we add the squared difference of the two values (word counts),
    # after which the final distance is the square root of this sum.
    # e.g. for 2d points (x1, y1), (x2, y2),
    # dist = sqrt((x1 - x2)^2 + (y1 - y2)^2)
    difference = novel1words - novel2words
    distance_squared = 0
    for x in difference:
        distance_squared += x * x

    return math.sqrt(distance_squared)

if __name__ == '__main__':
    novels, vocab = read_novels()
    clusters = random_clusters(novels, 8)

    for iteration in range(0, 4):
        total_distance = cluster_novels(novels, vocab, clusters)
        print "{}\t{}".format(iteration, total_distance)

    for cluster_id, cluster in enumerate(clusters):
        cluster = sorted(cluster, key=lambda x: x['author'])
        for novel_dict in cluster:
            print "C{}\t{} {} {}.".format(
                cluster_id,
                novel_dict['author'],
                novel_dict['title'],
                novel_dict['year']
            )
        print "----------------------------"
