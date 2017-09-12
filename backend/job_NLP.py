# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 04:39:38 2017

NLP algo to detect skills in each html doc

@author: stephen
"""
import os
indir = '/html_out' # Chris 12.09.2017 - take advantage of python's relative file path reading so this will work on any computer
filelist = []
for filenames in os.listdir(indir):
        if len(filenames) == 6:
            filenames = '0' + filenames
        if filenames[-5:] == '.html':
            filelist.append(filenames)
# sort files by ID number
filelist.sort()

for html_doc in range (0,len(filelist)):
    doc_file = os.path.join(indir, html_doc)
    with open(doc_file, 'r') as f:
        doc_words = f.readline()




##import module to connect to postgresql
#import psycopg2
##Connect to an existing database
#conn = psycopg2.connect("dbname ='Skilldb' user = 'postgres' host = 'localhost' password = 'postgres'")
##Open a cursor to perform database operations
#cur = conn.cursor()
##Query db to get extract data
#cur.execute("SELECT ...)
##going to need to actually add data into new column (job skill)... or new table w/ city... total skill..
##make changes persistent
#conn.commit()
##close db comm
#conn.close()
#
