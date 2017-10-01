# Important info

To run the backend code, you will need the following:
-Heroku database credentials in your .bashrc (or similiar depending on OS)
-The firebase credentials file in your home folder

## Mock Data
The mock data has been selected from various websites, see lines 14 - 23 in endpointwriter.py

# Backend Overview

*** Note that because of the modules, currently these scrips run only using ipython. It is planned to work with a normal terminal `python` command soon.

## Backend structure
database_writers/ - all scripts that write to the DB
  mongodbwriter.py - Writes objects to the Heroku mLab MongoDB in the form of {doc_id, HTML}
  endpointwriter.py - writes a line to the Heroku postgresql database per city with all endpoints (currently mock data)
  firebasewriter.py - reads all data from the Heroku database and (over)writes to the firebase database per city (uses the set() function, so any data set for a city will be the NEW data for that city)

natural_language/ - all scripts dealing with skill keyword finding and
  job_NLP.py - Natural language processing algorithm
  chris_NLP.py - Currently a failed attempt to find some skill keywords/phrases. Will be updated soon.

tasks/ - all scripts that relate to full processes - a full city pull, processing, and push to firebase, other summing of skills tasks. should be in cron scripts

raw_texts/ - in the local directory just to save any downloaded html files from the DB for (contents of which are in the .gitignore)

utils/ - utility modules used across the backend
  skillscout_connection_utilities.py - the only utility module (for now)

web_scraping/ - all scripts related to web_scraping
  jobscraper.py - Web Scraper
  secret_settings.py - some settings for scrapy

## Other files
full_proxy.txt - proxy settings for scrapy
README.md - this file.
