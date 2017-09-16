import os
from os.path import basename
import pymongo
from pymongo import MongoClient
import re

# MongoDB URI Connection
SKILLSCOUT_MONGODB_USER = os.environ.get("SKILLSCOUT_MONGODB_USER")
SKILLSCOUT_MONGODB_PASSWORD = os.environ.get("SKILLSCOUT_MONGODB_PASSWORD")
SKILLSCOUT_MONGODB_HOST = os.environ.get("SKILLSCOUT_MONGODB_HOST")
SKILLSCOUT_MONGODB_PORT = os.environ.get("SKILLSCOUT_MONGODB_PORT")
SKILLSCOUT_MONGODB_DB_NAME = os.environ.get("SKILLSCOUT_MONGODB_DB_NAME")

sMongoURI = "mongodb://" + SKILLSCOUT_MONGODB_USER + ":" + SKILLSCOUT_MONGODB_PASSWORD + "@" + SKILLSCOUT_MONGODB_HOST + ":" + SKILLSCOUT_MONGODB_PORT + "/" + SKILLSCOUT_MONGODB_DB_NAME

# client object
print "Connecting to MongoDB..."
client = MongoClient(sMongoURI)
print "Done."

# db - (lazy creation - db is created if it doesn't exist yet)
db = client[SKILLSCOUT_MONGODB_DB_NAME] # generated db name

# collection
oHTMLCollection = db['html-collection']

# write files to mongodb - loop over all html files
aHTMLFiles = []
for sFilename in os.listdir('./html_out/'):
    if sFilename.endswith('.html'):
        oFile = open('./html_out/%s' % sFilename) # file object
        sHTML = oFile.read() # get all html from the file
        sHTML = unicode(sHTML, errors='replace')
        sHTML = re.sub(r'\s+', ' ', sHTML) # clean up all the leftover whitespace with just a single space
        sDocId = basename(sFilename)
        aHTMLFiles.append({"doc_id": sDocId, "html": sHTML}) # insert file by file into db

# insert all HTML files into DB
print "Inserting into MongoDB..."
oHTMLCollection.insert_many(aHTMLFiles)
print "Done."
