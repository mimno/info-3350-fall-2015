from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
corpus = []

with open("sirgawain.txt") as f:
    for line in f:
        corpus.append(line.rstrip())

X = vectorizer.fit_transform(corpus)

print X.toarray()

print vectorizer.get_feature_names()
