import sys

"""
Problem 1: Read the docstring (the triple-quoted description
of the function) for word_count. Run the function in the
ipython interpreter using the incantation
    ipython -i A1.py sonnets.txt
and look at the output in word_count_dict. How many times
does 'thou' show up? How about 'Thou'? How many unique
tokens are there in word_count_dict? (Hint: len(x) returns
how many elements are in x).

Problem 2: Read the code below. What is the line
    if word is not in word_count_dict:
checking?

Problem 3: Read the documentation for the Counter class.
Import this class above and make word_count_dict a Counter
instead of a dictionary. Can you simplify the code? (Hint:
think about the update function for Counter.) What are the top
five most common tokens?

Problem 4: Find a string function that wll make every letter
in a string lowercase. Apply it to each line before splitting.
Use the method in Problem 1 to find out how many times we count
the token 'thou' now. How many unique tokens are there now?

Problem 5: Several tokens are being separated from tokens like
them because of neighboring punctuation: for instance, you might
notice that there is a token 'being' and a token 'being,'. One
solution to this is simply to remove all punctuation. Try this
using string.translate. (Hint: Look at string.punctuation.) How
many unique tokens are there now?

Problem 6: Sometimes, we still want to retain punction,
especially for contractions like "can't" that may contain
interesting information about language. Using string.strip,
remove only the punctuation at the beginning or the end of
each word. How many unique tokens are there now?

Problem 7: The Natural Language ToolKit (NLTK) has a number
of useful tools for tokenization. For instance, you can use
the Stanford tokenizer in NLTK with the following import:
    from nltk.tokenize.stanford import StanfordTokenizer
which will allow you to create StanfordTokenizer objects
that you can use to tokenize strings. Create a StanfordTokenizer
and replace the code breaking a line into words with a call to
StanfordTokenizer's tokenize() function. How many unique tokens
are there now? How about if you make every token lowercase?
Are there tokens you wouldn't want to count?
(see nltk.org/api/nltk.tokenize.html for example code)

Problem 8: Try running this code on the Urdu text snippet.
Does it work? How would you tweak it to work better? Feel free
to look up information about how to do this on StackOverflow,
the Python documentation, and other Google-able sources.

"""
def word_count(filename):
    """A function that returns a dictionary with tokens as keys
    and counts of how many times each token appeared as values in
    the file with the given filename.

    Inputs:
        filename - the name of a plaintext file
    Outputs:
        A dictionary mapping tokens to counts.
    """

    word_count_dict = {}

    with open(filename, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                if word not in word_count_dict:
                    word_count_dict[word] = 1
                else:
                    word_count_dict[word] += 1

    return word_count_dict


if __name__ == '__main__':
    word_count_dict = word_count(sys.argv[1])
