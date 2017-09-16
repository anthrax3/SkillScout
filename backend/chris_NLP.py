import psycopg2
import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from rake_nltk import Rake

# DB Credentials (in bashrc)
DB_NAME = os.environ.get("SKILLSCOUT_DB_NAME")
DB_USER = os.environ.get("SKILLSCOUT_DB_USER")
DB_PASSWORD = os.environ.get("SKILLSCOUT_DB_PASSWORD")
DB_HOST = os.environ.get("SKILLSCOUT_DB_HOST")
DB_PORT = os.environ.get("SKILLSCOUT_DB_PORT")
##########################################
### Connect to DB and get all keywords ###
##########################################
print "Connecting, retreving keywords, and closing..."
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) # connect to db
cur = conn.cursor() # Open a cursor to perform database operations
cur.execute("SELECT * FROM keywords;")
tKeywords = cur.fetchall()
conn.close()
print "Done."

# constants
r = Rake()
lKeywords = [i[0] for i in tKeywords] # covert list of singular tuples to list
cachedStopWords = stopwords.words("english")
porter = nltk.PorterStemmer() # porter stemmer
lStemmedKeywords = [porter.stem(t) for t in lKeywords] # stem all the keywords

# definitions

### retuns an array of all indexes where a match is found
def findIndexes(lList, sVal):
    return [i for i, x in enumerate(lList) if x == sVal]

### prints preceding and following words around keywords in the text
def findSkills(sHTML, sMethod):
    oSoup = BeautifulSoup(sHTML, "html5lib") # BeautifulSoup the html!
    [s.extract() for s in oSoup('head')] # remove everything in <head> tag
    [s.extract() for s in oSoup('script')] # remove everything in <script> tags
    [s.extract() for s in oSoup('noscript')] # remove everything in <noscript> tags
    sText = oSoup.text # get raw text left in article
    sText.lower() # convert any uppercase letters to lowercase
    sText = re.sub(r'\s+', ' ', sText) # clean up all the leftover whitespace with just a single space
    sText = sText.encode('utf-8')
    sText = ' '.join([word for word in sText.split() if word not in cachedStopWords]) # use nltk to remove stop words
    if sMethod == "RAKE_RANKED_PHRASES":
        r.extract_keywords_from_text(sText)
        print r.get_ranked_phrases();
    if sMethod == "RAKE_SCORED_PHRASES":
        r.extract_keywords_from_text(sText)
        print r.get_ranked_phrases_with_scores();
    if sMethod == "CUSTOM":
        lText = sText.split() # split text into an array
        lTokenText = nltk.word_tokenize(sText)
        lTaggedText = nltk.pos_tag(lTokenText)
        lStemmedText = [porter.stem(t) for t in lTokenText] # porter stemmer to (matched with stemmed key words)
        # for each of the keywords, find the index of those keywords and print the word in front and after it
        for sKeyword in lStemmedKeywords:
            lKeywordIndexes = findIndexes(lStemmedText, sKeyword) # find indexes of keyword
            print sKeyword
            for iIndex in lKeywordIndexes:
                print(str(lTaggedText[iIndex-2][0]),  " ",  str(lTaggedText[iIndex-1][0]),  " ",  str(lTaggedText[iIndex+1][0]),  " ",  str(lTaggedText[iIndex+2][0]))
    if sMethod == "FREQUENCY":
        words = sText.split()

        # Get the set of unique words.
        uniques = []
        for word in words:
          if word not in uniques:
            uniques.append(word)

        # Make a list of (count, unique) tuples.
        counts = []
        for unique in uniques:
          count = 0              # Initialize the count to zero.
          for word in words:     # Iterate over the words.
            if word == unique:   # Is this word equal to the current unique?
              count += 1         # If so, increment the count
          counts.append((count, unique))

        counts.sort()            # Sorting the list puts the lowest counts first.
        counts.reverse()         # Reverse it, putting the highest counts first.
        # Print the ten words with the highest counts.
        for i in range(min(50, len(counts))):
          count, word = counts[i]
          print('%s %d' % (word, count))

###########################
### Main Program Proces ###
###########################

# loop over all html files
for filename in os.listdir('./html_out/'):
    if filename.endswith('.html'):
        oFile = open('./html_out/%s' % filename) # file object
        sHTML = oFile.read() # get all html from the file
        findSkills(sHTML, "RAKE_SCORED_PHRASES")
