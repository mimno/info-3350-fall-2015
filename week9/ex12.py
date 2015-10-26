# -*- coding: utf-8 -*-
"""
Exercise 12, Topic Modeling

Most of the work you will do is going to be web-based
in a Javascript application. This file contains a 
Python script that just starts a local webserver.

Questions:

. We started with a "default" stoplist.txt file. Which
words would you want to remove for this corpus? Which
are you conflicted about? Why?

. Describe the "meaning" of a topic (ie what real-world
theme does it correspond to?) based on just the top-ranked
words. Now look at the top-ranked documents for that
topic. Does the document view change your impression
of the topic? How?

. What do you know about the collection based on the
topic browser? What are the main themes? How do 
these compare to the categories listed in the
documents.txt file?


"""

import SimpleHTTPServer
import SocketServer

PORT = 8002

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()