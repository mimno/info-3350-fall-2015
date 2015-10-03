"""
Name:

This week, we'll look at clustering novels based on the k-nearest-neighbors
(KNN) clustering method.
"""

from collections import Counter
# Tell python we need the natural language toolkit and 
#  a particular type of tokenizer.
import math
from nltk.tokenize import RegexpTokenizer


def read_novels():
    novels = []
    tokenizer = RegexpTokenizer("\w+('\w+)?")
    vocab = Counter()
    
    # This reads in every novel's metadata
    with open("metadata.tsv") as metafile:
        for novel_data_line in metafile:
            filename, title, author, year, _ = novel_data_line.split('\t', 4)
            word_counter = Counter()
            # The metadata gives us the filename from which we can
            # get our word counts
            with open(filename) as novelfile:
                for line in novelfile:
                    lowerline = line.lower()
                    words = tokenizer.tokenize(lowerline)
                    vocab.update(words)
                    word_counter.update(words)
            # We're tracking four of the fields for each novel
            novels.append({
                'title': title,
                'author': author,
                'year': year,
                'words': word_counter
            })

    # Could we do something smarter here?
    top_vocab = [v for (v, i) in vocab.most_common(10000)]
    return novels, top_vocab


def cluster_novels(novels, vocab, k):
    n_novels = len(novels)
    
    novel_distances = []
    for novel1 in novels:
        novel_line = []
        for novel2 in novels:
            novel_line.append(novel_distance(novel1, novel2))
        novel_distances.append(novel_line)

def novel_distance(novel1, novel2, vocab):
    # We're starting with Euclidean distance, or L2 distance:
    # for each dimension (in this case, for each word type),
    # we add the squared difference of the two values (word counts),
    # after which the final distance is the square root of this sum.
    # e.g. for 2d points (x1, y1), (x2, y2),
    # dist = sqrt((x1 - x2)^2 + (y1 - y2)^2)
    distance_squared = 0
    for word in vocab:
        distance_squared += (novel1['words'][word] - novel2['words'][word])^2

    # Do we actually have to do this next step?
    distance = math.sqrt(distance_squared)
    return distance_squared


if __name__ == '__main__':
    novels, vocab = read_novels()
    with open('novel_count_file.tsv', 'w') as novel_ct_file:
        novel_ct_file.write('{}\t{}\t{}\t{}\n'.format('title', 'author', 'year', '\t'.join(vocab)))
        for novel in novels:
            wd_cts = [str(novel['words'][word]) for word in vocab]
            novel_ct_file.write('{}\t{}\t{}\t{}\n'.format(
                novel['title'],
                novel['author'],
                novel['year'],
                '\t'.join(wd_cts)))
            
