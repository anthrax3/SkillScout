# Important info

To run the backend code, you will need the following:
-Heroku database credentials in your .bashrc (or similiar depending on OS)
-The firebase credentials file in your home folder

## Mock Data
The mock data has been selected from various websites, see lines 14 - 23 in endpointwriter.py

# Backend Overview

## Python files
jobscraper.py - Web Scraper
job_NLP.py - Natural language processing algorithm
chris_NLP.py - Currently a failed attempt to find some skill keywords/phrases. Will be updated soon.
mongodbwriter.py - Writes objects to the heroku mLab MongoDB in the form of {doc_id, HTML}
endpointwriter.py - writes a line to the Heroku postgresql database per city with all endpoints (currently mock data)
firebasewriter.py - reads all data from the Heroku database and (over)writes to the firebase database per city (uses the set() function, so any data set for a city will be the NEW data for that city)
secret_settings.py - some settings for scrapy

## Other files
full_proxy.txt - proxy settings for scrapy
README.md - this file.
