import re
import nltk
import sys
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import PostgresqlDB
from utils.skillscout_connection_utilities import MongoDB
from utils.skillscout_connection_utilities import cleanHTML
from nltk.corpus import stopwords
from rake_nltk import Rake

# mongodb DB object
oMongoDB = MongoDB()

# collection
oHTMLCollection = oMongoDB.db['html-collection']

##########################################
### Connect to DB and get all keywords ###
##########################################
print "Connecting, retreving keywords, positive phrases, negative phrases, and closing..."
oPostgresql = PostgresqlDB()
oPostgresql.execute("SELECT * FROM keywords;","") # note the params parameter can be just an empty string here
tKeywords = oPostgresql.fetchall()
oPostgresql.execute("SELECT * FROM positive_phrases;","") # note the params parameter can be just an empty string here
tPositivePhrases = oPostgresql.fetchall()
oPostgresql.execute("SELECT * FROM negative_phrases;","") # note the params parameter can be just an empty string here
tNegativePhrases = oPostgresql.fetchall()
oPostgresql.close()
print "Done."

# variables
r = Rake()
lKeywords = [i[0] for i in tKeywords] # covert list of singular tuples to list
lPositivePhrases = [i[0] for i in tPositivePhrases] # covert list of singular tuples to list
lNegativePhrases = [i[0] for i in tNegativePhrases] # covert list of singular tuples to list
cachedStopWords = stopwords.words("english")
porter = nltk.PorterStemmer() # porter stemmer
lStemmedKeywords = [porter.stem(t) for t in lKeywords] # stem all the keywords

# definitions

### retuns an array of all indexes where a match is found
def findIndexes(lList, sVal):
    return [i for i, x in enumerate(lList) if x == sVal]

### prints preceding and following words around keywords in the text
def findSkills(sText, sMethod):
    ### BEGIN METHOD CHOICE ###
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
    if sMethod == "PHRASES":
        # positive key phrases: loop over all positive key phrases and regex out the key sentances
        print "Positive Phrases:"
        for sPositivePhrase in lPositivePhrases:
            sRegexString = sPositivePhrase + " (.*?)\." # build regex string to query the text (everything between phrase and end of sentance)
            for result in re.findall(sRegexString, sText, re.S): # re.S is the DOTALL flag, meaning even if a newline is inbetween the delimiters, it picks it up
                # for each sentence found from our regex
                print sPositivePhrase + ": " + result

        # positive key phrases: loop over all positive key phrases and regex out the key sentances
        print "Negative Phrases:"
        for sNegativePhrase in lNegativePhrases:
            sRegexString = sNegativePhrase + " (.*?)\." # build regex string to query the text (everything between phrase and end of sentance)
            for result in re.findall(sRegexString, sText, re.S): # re.S is the DOTALL flag, meaning even if a newline is inbetween the delimiters, it picks it up
                # for each sentence found from our regex
                print sNegativePhrase + ": " + result

###########################
### Main Program Proces ###
###########################

# loop over all html data in
for oHTMLEntry in oHTMLCollection.find():
    sHTML = oHTMLEntry['html'] # we only need the html component
    sText = cleanHTML(sHTML) # clean the raw html
    sText = ' '.join([word for word in sText.split() if word not in cachedStopWords]) # use nltk to remove stop words
    findSkills(sText, "PHRASES")
