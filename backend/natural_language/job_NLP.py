# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 04:39:38 2017

NLP algo to detect skills in each html doc

@author: stephen
"""
import os
current_path = os.path.dirname(os.path.realpath('__file__'))
print 'input directory must be in SkillScout/backend/web_scraping/ and in the directory and named "html_out"
input_dir = os.path.join(current_path,'../../web_scraping/html_out')
filelist = []
for filenames in os.listdir(indir):
        if len(filenames) == 6:
            filenames = '0' + filenames
        if filenames[-5:] == '.html':
            filelist.append(filenames)
# sort files by ID number
filelist.sort()
#Enter each doc and read txt.
for html_doc in range (len(filelist)):
    if html_doc < 10:
        filelist = filelist[html_doc][1:]
    else:
        filelist = filelist[html_doc]
    doc_file = os.path.join(indir, filelist)
    with open(doc_file, 'r') as f:
        doc_words = f.read().replace('\n', '')
      #find if string exists: 
      #index given if found, -1 otherwise
      #can be used to find if skill exists, not where tho '
        search_word = 'require'
        word_exists = any(search_word in doc_words for x in doc_words)
       #if word_exists = True:
       # else:
       # use regexp to find loc. of all words


           
           
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
