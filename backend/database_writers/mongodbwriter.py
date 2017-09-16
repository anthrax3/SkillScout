import sys
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import MongoDB
import os
from os.path import basename
import re

# connect to mongodb
oMongoDB = MongoDB()

# collection
oHTMLCollection = oMongoDB.db['html-collection']

# write files to mongodb - loop over all html files
aHTMLFiles = []
for sFilename in os.listdir('./html_out/'):
    if sFilename.endswith('.html'):
        oFile = open('./html_out/%s' % sFilename) # file object
        sHTML = oFile.read() # get all html from the file
        sHTML = unicode(sHTML, errors='replace')
        sHTML = re.sub(r'\s+', ' ', sHTML) # clean up all the leftover whitespace with just a single space
        sCity, sDocId = basename(sFilename).split('-')
        aHTMLFiles.append({"city": sCity, "doc_id": sDocId, "html": sHTML}) # insert file by file into db

# insert all HTML files into DB
print "Inserting into MongoDB..."
oHTMLCollection.insert_many(aHTMLFiles)
print "Done."
