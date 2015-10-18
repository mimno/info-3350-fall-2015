"""
Name:

Code adapted from Joseph Wilk's semanticpy github, specifically
https://github.com/josephwilk/semanticpy/blob/master/semanticpy/transform/lsa.py

What to try:

1. Try changing how many of the words we keep. How much does it change our
similarities? How about our "topics"?

2. Are the "topics" actually topics? What does this tell us about our
new dimensions?

3. Can we change which novels we consider to deal better with
volumes of the same novel by zeroing out similarities for other
pairs? Try changing the "if i == j" line to something relating
to novel and othernovel.

4. How low can we set the dimension before it stops producing the
results we expect / how many dimensions do we "need"?

5. In the wild, we don't use LSA on raw matrices, but instead normalize
them based on how "important" words are, where words that show up a lot
in a particular document and rarely otherwise are useful. There are tools
that do this for us from document-word counts, notably the
sklearn.feature_extraction.text.TfidfTransformer. Read the documentation
for this and see if you can apply it to the original document-word matrix.
"""

import csv
import numpy as np
from scipy import dot
from scipy import linalg
from scipy.spatial.distance import cosine


def read_novels():
    """Read in a file describing metadata and word counts for a number
    of novels, returning the vocabulary, novel metadata, and a matrix of
    word counts for each novel and each word in the vocabulary."""
    novels = []
    
    # This reads in every novel's metadata and word counts for the 10000
    # most frequent words
    with open("novel_count_file.tsv") as novelfile:
        novel_reader = csv.reader(novelfile, delimiter='\t') 
        
        # We find the titles for each of the rows, including the word list
        header_line = novel_reader.next()
        vocab = header_line[3:]
        novelmatrix = []

        # We read each novel into a dictionary
        for novel_data_line in novel_reader:
            title, author, year = novel_data_line[:3]
            
            ## everything from index 3 on is a string
            ##  representing a word count
            count_strings = novel_data_line[3:]
            word_count_list = np.zeros(len(count_strings))

            for i in range(0, len(count_strings)):
                word_count_list[i] = float(count_strings[ i ])

            # We're just going to grab the metadata for each novel
            # for our list of novels
            novels.append({
                'title': title,
                'author': author,
                'year': year,
            })
            # We'll put the actual words into a matrix, where the
            # ith row is word counts for the ith novel in novels
            novelmatrix.append(word_count_list)

        # We're also going to convert this to a nifty format
        # for doing math things to it
        novelmatrix = np.array(novelmatrix)
        return vocab, novels, novelmatrix

def lsa(document_word_matrix, dimension):
    """
    Take a document-word matrix and retrieve document-concept and concept-word
    matrices from it using latent semantic analysis (LSA).
    """
    # We need to know the shape of our starting document-word matrix in
    # terms of number of rows and columns in order to run LSA.
    rows, cols = document_word_matrix.shape

    # We can't create a matrix bigger than what we started with
    if dimension > rows:
        raise ValueError("Dimension {} too big!".format(dimension))

    # Dimensions also have to be positive
    elif dimension < 1:
        raise ValueError("Dimension {} too small!".format(dimension))

    # We use singular value decomposition to decompose our original
    # document-word matrix into three matrixes that, multiplied together,
    # recreate our original:
    # - word_topic: a matrix with m terms as rows and r "concept"
    #   proportions as columns,
    # - singular_values: a nonnegative diagonal matrix of r rows and r 
    #   columns, and
    # - topic_document: a matrix with r "concepts" as rows and n documents
    #   as columns.
    # Because the singular_values matrix actually only has values on the 
    # diagonal, we just get it as a list of r singular values that would be
    # the diagonal of the matrix in order from greatest to least.
    word_topic, singular_values, topic_document = linalg.svd(document_word_matrix)

    # Our goal is to reduce the original dimensions of this to the number
    # of concepts or "topics" we want, which we do by discarding all of the
    # columns and rows corresponding to values we don't need. This is
    # straightforward for our word-topic matrix: we throw out all of the
    # columns past the dimension we want.
    lsa_singular_values = singular_values[:dimension]
    lsa_word_topic = word_topic[:,:dimension]
    
    # Our topic-document matrix is a little trickier, because we'd rather
    # have our documents as rows and topics as columns, and right now it's
    # the other way around. So we'll switch it or transpose it.
    lsa_topic_document = topic_document[:dimension,:]
    lsa_document_topic = np.transpose(lsa_topic_document)

    # We can check that we did things right by using our new matrices
    new_singular_matrix = linalg.diagsvd(lsa_singular_values, dimension, dimension)
    transformed_matrix = dot(dot(lsa_word_topic, new_singular_matrix), lsa_topic_document)
    
    # We know that SVD gives us in our singular value matrix the values we care
    # about in order.
    print "Representation error: {}".format(np.sum((document_word_matrix - transformed_matrix)**2))

    return lsa_word_topic, lsa_document_topic

if __name__ == '__main__':
    # We'll run LSA with a reduction to 20 dimensions. What happens if you use
    # more?
    dimension = 20
    # We're also providing the option to throw away the first K words of the
    # vocabulary, but we're starting it at 0.
    word_offset = 0
    vocab, novels, novelmatrix = read_novels()
    
    lsa_word_topic, lsa_doc_topic = lsa(novelmatrix[:,word_offset:], dimension)
    
    # Right now, we're finding which novels are most similar based on the cosine
    # similarity (a measure of similarity based on how big the cosine is between
    # the two lists of numbers as vectors). We expect most novels to be most
    # similar to the other volumes in the same set, which we can validate here
    # by removing similarity scores for novels and themselves (which will be 1)
    # and finding the novel most similar besides itself.
    sims = np.array([
        [1 - cosine(novelmatrix[i], novelmatrix[j]) for j in range(len(novels))]
        for i in xrange(len(novels))]
    )

    print "Most similar novels:"
    for i, novel in enumerate(novels):
        for j, othernovel in enumerate(novels):
            # We remove each novel from being in consideration for most similar
            # to itself by zeroing out the similarity in the matrix.
            # How could we rewrite this to remove similarities from other
            # similarities we don't care about, like novels with almost
            # with almost the same title or with the same author?
            if i == j:
                sims[i][j] = 0
        best = np.argmax(sims[i])
        # We print out the novel most similar for each book. Is this most-
        # similar metric symmetric (if novel A is most similar to novel B, is B
        # most similar to novel A)? Why or why not?
        print '  Novel {}: {} -- {}\n             {} -- {}'.format(i, novel['author'], novel['title'], novels[best]['author'], novels[best]['title'])

    # We're going to print out the top 20 words for each "topic".
    # Do these actually look like topics?    
    print "Words for each 'topic':"
    lsa_topic_word = np.transpose(lsa_word_topic)
    for dim in range(dimension):
        best_word_indices = []        
        for i in range(20):
            # Find the best word, then set it to -inf
            bestwd = np.argmax(lsa_topic_word[dim])
            best_word_indices.append(bestwd)
            lsa_topic_word[dim][bestwd] = float('-inf')
        print '  Topic {}: {}'.format(dim, ' '.join([vocab[word_offset:][wd] for wd in best_word_indices]))