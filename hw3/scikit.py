# -*- coding: utf-8 -*-
"""
Name:
NetID:

This assignment aims at showing some of the tools available in scikit-learn,
a machine learning package implementing many of our favorite machine learning
tools. While it can be an awesome resource to avoid rewriting the algorithms
we've talked about in this class, the functions you use to get these models
to work are at first a little odd, so we want you to get used to reading the
documentation for these and figuring out which functions do what you want and
what arguments you need.

Problem 1. (3 pts) The first function, get_2d_cluster, generates
points from a Gaussian distribution. What is a Gaussian distribution?
What do mu and sigma control? Look this up somewhere and provide your
source.

Answer:

Problem 2. (5 pts) Change the code defining labels_predicted to
use the GaussianNB object gnb to fit a Naive Bayes model to the training
data and then define labels_predicted as the predicted labels of that
model on the test points. What is the success rate? Is it consistent?

Answer:

Problem 3: (5 pts) Change the code defining labels_clustered to use the
KMeans object km to fit three clusters using the K-means algorithm and
return the predicted labels of each point.

Problem 4: (5 pts) Copy the code for plotting the original clusters and
paste it at the end of the file. Rewrite it to use labels_clustered
instead of the original labels.

Problem 5: (2 pts) Look at the resulting figure. How does it differ
from the original clustering?

"""

from random import gauss
from matplotlib import pyplot as plt

# We're going to use these to make figures
# of our points
colorlist = ['#FF0000', '#00FF00', '#0000FF']

# This is a little helper function that generates points in a
# Gaussian distribution (a bell curve in multiple dimensions).
def get_2d_cluster(mu_x, mu_y, sigma, k):
    pts = []
    for i in xrange(k):
        pts.append((gauss(mu_x, sigma), gauss(mu_y, sigma)))
    return pts

# We're going to generate three clusters: two little separate ones
# and one big one
points = []
labels = []

# Cluster 0
points += get_2d_cluster(1.0, 1.0, 0.5, 100)
labels += [0] * 100

# Cluster 1
points += get_2d_cluster(1.0, -1.0, 0.5, 100)
labels += [1] * 100

# Cluster 2
points += get_2d_cluster(-1.0, 0, 1, 300)
labels += [2] * 300

# Here, we plot our original clusters.
xs = [p[0] for p in points]
ys = [p[1] for p in points]
color = [colorlist[i] for i in labels]
plt.scatter(xs, ys, color=color)
plt.show()

# Here, we get a train and a test split for our data using scikit-learn.
from sklearn.cross_validation import train_test_split
points_train, points_test, labels_train, labels_test = train_test_split(
    points, labels, test_size = 0.2
)

# Here, we get a Naive Bayes Classifier trained on our training data and
# test how well it predicts other points.
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
# Modify the line below to use the GaussianNB object gnb
# to fit a Naive Bayes model to our training data and then
# predict the labels of our test data points.
labels_predicted = [-1] * 500
successes = 0.0
for act, pos in zip(labels_test, labels_predicted):
    if act == pos:
        successes += 1
print "Success rate:", successes / len(labels_test)

# Here, we do a k-means clustering of all of our points.
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
# Fix this line so that it uses the KMeans object km to produce
# the predictions of which cluster each point is in after fitting
# the clusters to all of our point data without providing labels.
labels_clustered = []

# Copy the code from the original cluster plots and
# modify it slightly to use our new labels