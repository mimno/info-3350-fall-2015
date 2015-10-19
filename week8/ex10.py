"""
Name:

Code adapted from Joseph Wilk's semanticpy github, specifically
https://github.com/josephwilk/semanticpy/blob/master/semanticpy/transform/lsa.py

What to try:

1. Pick some words from the vocabulary. What are the most similar words?
Do these make sense? (Try "letter" or "the")

[ANSWER HERE]

2. Pick a few novels, and find their most similar novels. We're printing the
titles with their ID numbers for reference. Try 113 ("The Italian").

[ANSWER HERE]

3. Try changing how many of the words we keep. How much does it change our
similarities? How about our "topics"?

[ANSWER HERE]

4. Are the "topics" actually topics? What does this tell us about our
new dimensions? Use the topic_words() function.

[ANSWER HERE]

5. How low can we set the dimension before it stops producing the
results we expect / how many dimensions do we "need"?

[ANSWER HERE]

"""

import csv
import numpy as np
from scipy import dot
from scipy import linalg

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
        line_number = 0

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
                'id': line_number,
                'title': title,
                'author': author,
                'year': year,
            })
            # We'll put the actual words into a matrix, where the
            # ith row is word counts for the ith novel in novels
            novelmatrix.append(word_count_list)
            
            line_number += 1

        # We're also going to convert this to a nifty format
        # for doing math things to it
        novelmatrix = np.transpose(np.array(novelmatrix))
        
        return vocab, novels, novelmatrix

def lsa(document_word_matrix, dimension):
    """
    Take a document-word matrix and retrieve document-concept and concept-word
    matrices from it using latent semantic analysis (LSA).
    """
    # We need to know the shape of our starting document-word matrix in
    # terms of number of rows and columns in order to run LSA.
    rows, cols = document_word_matrix.shape

    #for row in range(rows):
    #    document_word_matrix[row,:] /= math.sqrt()

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
    print singular_values

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

def closest_words(query):
    row_norms = np.sqrt(np.sum(lsa_word_topic**2, axis=1))
    query_index = vocab.index(query)
    query_vector = lsa_word_topic[query_index]
    cosines = np.divide(np.dot(lsa_word_topic, query_vector), row_norms)
    
    return sorted(zip(cosines, vocab), reverse=True)
    
def closest_docs(query_index):
    row_norms = np.sqrt(np.sum(lsa_doc_topic**2, axis=1))
    query_vector = lsa_doc_topic[query_index]
    cosines = np.divide(np.dot(lsa_doc_topic, query_vector), row_norms)
    
    return sorted(zip(cosines, [novel["title"] for novel in novels]), reverse=True)
    
def topic_words(col):
    return sorted(zip(lsa_word_topic[:,col], vocab), reverse=True)

if __name__ == '__main__':
    # We'll run LSA with a reduction to 20 dimensions. What happens if you use
    # more?
    dimension = 20
    # We're also providing the option to throw away the first K words of the
    # vocabulary, but we're starting it at 0.
    word_offset = 0
    vocab, novels, novelmatrix = read_novels()
    
    lsa_word_topic, lsa_doc_topic = lsa(novelmatrix[:,word_offset:], dimension)
    
    print [(novel["id"], novel["title"]) for novel in novels]

    