# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:28:49 2015

Problem 1. (5 pts) The first function, get_2d_cluster, generates
points from a Gaussian distribution. What is a Gaussian distribution?
What do mu and sigma control? Look this up somewhere and provide your
source.

Answer:

Problem 2. (5 pts) 
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

# Here, we plot our original clusters
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
labels_predicted = gnb.fit(points_train, labels_train).predict(points_test)
successes = 0.0
for act, pos in zip(labels_test, labels_predicted):
    if act == pos:
        successes += 1
print "Success rate:", successes / len(labels_test)

# Here, we do a k-means clustering of the points we have, ignoring the
# labels from before.
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
labels_clustered = km.fit_predict(points)

# Here, we plot our three K-means clusters
color = [colorlist[i] for i in labels_clustered]
plt.scatter(xs, ys, color=color)
plt.show()