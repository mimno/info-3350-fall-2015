"""
Name:

This week, we'll look at clustering novels based on the agglomerative
clustering method.

1. Go look through the metadata file a bit, specifically at the first few
fields of each line. Does this data help us? How could it be more useful?

2. Run the clustering algorithm. Do the clusters seem reasonable? How could
you tell?

3. Try changing the number of clusters. How does this change?

4. Look at the distance function. Right now, we're using Euclidean (L2)
distance. Try out another type of distance (cosine distance, L1 distance,
etc.) If you're not familiar with these types of distance, look them up
and check them out - some have implementations in the scipy python package
already. Does this change your clustering?

5. Look at how we pick which two clusters to join. Are there other ways
we could do this?
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
            novels.append({
                'title': title,
                'author': author,
                'year': year,
                'words': word_count_list
            })

    print "Loaded {} novels, using vocab {}".format(len(novels), len(vocab))
    return novels, vocab


def cluster_novels(novels, vocab, k):
    n_novels = len(novels)
    
    # We start out by computing all the distances between points - it'll
    # make it faster later.
    novel_distances = []
    for novel1 in novels:
        novel_line = []
        for novel2 in novels:
            # novel_distances[a][b] for ints a and b will be the distance
            # between the ath and bth novels, or None if a and b are equal
            dist = None
            if novel1 != novel2:
                dist = novel_distance(novel1['words'], novel2['words'])
            novel_line.append(dist)
        novel_distances.append(novel_line)

    # The cluster number each point belongs to. At the start, each belongs
    # to its own cluster.
    cluster_assign = range(n_novels) 

    # After each iteration, novel_distances[a][b] for ints a and b will be
    # the distance between the ath and bth novels if they're not in the same
    # cluster or None if they are.
   
    print "Running {} iterations".format(n_novels - k)
    # We will join two clusters in each iteration of this loop. Why do we get
    # k clusters after doing this n_novels - k times?
    for iter in range(n_novels - k):
        # We pick the clusters to join by finding which two points that aren't
        # in the same cluster are closest together.
        min_dist = float('inf')
        min_indices = (None, None)

        # enumerate() is a function that takes in something we can iterate
        # through - a dictionary, a list, etc. - and turns it into pairs of
        # a number and the item from that iterable thing, where the number
        # counts up from 0. For instance, if li = ['foo', 'bar'],
        # then enumerate(li) = [(0, 'foo'), (1, 'bar')]. This helps when
        # we want to keep track of things as numbers instead of full values:
        # we can refer to each of our novels by a single number for most of
        # this code instead of the full novel dictionary.
        for novel1, novel_row in enumerate(novel_distances):
            # First we find the minimum value in the row
            min_row_dist = min([n for n in novel_row if n is not None])
            # If it's the best min value we've seen so far, we'll
            # find the index for the novel whose distance from novel1
            # this corresponds to and update our "best so far" min_dist
            # and min_indices.
            if min_row_dist < min_dist:
                min_dist = min_row_dist
                novel2 = novel_row.index(min_row_dist)
                min_indices = (novel1, novel2)
    
        # We now have two indices of novels whose clusters we should join.
        # We want to find all the novels with those two cluster numbers,
        # put them into the same number, and make sure they all have None
        # as their distances
        index1 = cluster_assign[min_indices[0]]
        index2 = cluster_assign[min_indices[1]]
        cluster1 = []
        cluster2 = []
        for nov, clus in enumerate(cluster_assign):
            if clus == index1:
                cluster1.append(nov)
            elif clus == index2:
                cluster2.append(nov)
        
        # Now that we know what's in each cluster, we take each pair of
        # points with one in each cluster and set their in-between distance
        # to None.
        for nov1 in cluster1:
            for nov2 in cluster2:
                novel_distances[nov1][nov2] = None
                novel_distances[nov2][nov1] = None

        # Finally, we set all the points in cluster2 to be in cluster1
        for nov in cluster2:
            cluster_assign[nov] = index1

    # Now we can return our clusters as lists.
    final_cluster_dict = defaultdict(list)
    for nov, novel_dict in enumerate(novels):
        final_cluster_dict[cluster_assign[nov]].append(novel_dict)
    
    return final_cluster_dict
        

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


if __name__ == '__main__':
    novels, vocab = read_novels()
    final_cluster_dict = cluster_novels(novels, vocab, 10)
    print len(final_cluster_dict), "clusters found"
    for cluster_no, cluster in enumerate(final_cluster_dict.values()):
        print "Cluster {0}:".format(cluster_no)
        cluster = sorted(cluster, key=lambda x: x['author'])
        for novel_dict in cluster:
            print "    {} {} {}.".format(
                novel_dict['author'],
                novel_dict['title'],
                novel_dict['year']
            )
