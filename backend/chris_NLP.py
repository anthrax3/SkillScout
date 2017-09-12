import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# constants
cachedStopWords = stopwords.words("english")

# loop over all html files
for filename in os.listdir('./html_out/'):
    if filename.endswith('.html'):
        oFile = open('./html_out/%s' % filename) # file object
        sHTML = oFile.read() # get all html from this
        oSoup = BeautifulSoup(sHTML, "html5lib") # BeautifulSoup it!
        [s.extract() for s in oSoup('head')] # remove everything in <head> tag
        [s.extract() for s in oSoup('script')] # remove everything in <script> tags
        [s.extract() for s in oSoup('noscript')] # remove everything in <noscript> tags
        sText = oSoup.text # get just raw text left in article
        sText = re.sub(r'\s+', ' ', sText) # clean up all the leftover whitespace with just a single space
        print sText
        sText = ' '.join([word for word in sText.split() if word not in cachedStopWords]) # use nltk to remove stop words
        print sText
        lTokenText = nltk.word_tokenize(sText)
        lTaggedText = nltk.pos_tag(lTokenText)
        print lTaggedText
        lNounText = [t[0] for t in lTaggedText if t[1] == "NN"]
        print lNounText


        # count of words
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
