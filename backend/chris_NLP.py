import glob
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)

# loop over all html files
for filename in glob.iglob('/html_out/*.html'):
     oFile = open('/html_out/%s' % filename) # file object
     sHTML = oFile.read() # get all html from this
     soup = BeautifulSoup(sHTML) # BeautifulSoup it!
     soup('head').extract() # remove everything in <head> tag
     soup('script').extract() # remove everything in <script>
     sText = strip_tags(soup) # now we have just the raw text of the article
     print sText
