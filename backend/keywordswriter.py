# imports
import os
import psycopg2

# DB Credentials (in bashrc)
DB_NAME = os.environ.get("SKILLSCOUT_DB_NAME")
DB_USER = os.environ.get("SKILLSCOUT_DB_USER")
DB_PASSWORD = os.environ.get("SKILLSCOUT_DB_PASSWORD")
DB_HOST = os.environ.get("SKILLSCOUT_DB_HOST")
DB_PORT = os.environ.get("SKILLSCOUT_DB_PORT")

# keywords to help look in text (add to this as we see fit)
keywords =  ["required","able","ability","should","will","need","not","want","looking","responsibilities","include","relevant","experience","seeking"]

################################################################
### Connect to DB and get all cities / endpoints for website ###
################################################################
print "Connecting..."
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) # connect to db
cur = conn.cursor() # Open a cursor to perform database operations
print "Done."

# query string (seperated into multiple lines for readability, same for every city loop)
sQuery = "INSERT INTO keywords (keyword) VALUES (%s) ON CONFLICT (keyword) DO NOTHING"

for i in range(0, len(keywords)):
    # write the skill into the DB
    cur.execute(sQuery, (keywords[i],)) # note the weird () with the , is required for psycopg2 syntax...
    print "Keyword data line " + str(i) + " of " + str(len(keywords)) + " complete..."

# done with loop of transactions, commit them to the db
print "Commiting..."
conn.commit()
print "Done."
conn.close()
print "Connection closeed."
