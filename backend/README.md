# Important info

To run this code, you will need the following:
-Heroku database credentials in your .bashrc (or similiar depending on OS)
-The firebase credentials file in your home folder

# Backend Overview

## Files
jobscraper.py - Web Scraper
job_NLP.py - Natural language processing algorithm
endpointwriter.py - writes a line to the Heroku postgresql database per city with all endpoints (currently mock data)
firebasewriter.py - reads all data from the Heroku database and (over)writes to the firebase database per city (uses the set() function, so any data set for a city will be the NEW data for that city)
