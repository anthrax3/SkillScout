# imports
import sys
sys.path.insert(0,"../utils")
from utils import skillscout_connection_utilities

# keywords to help look in text (add to this as we see fit)
keywords =  ["required","able","ability","should","will","need","not","want","looking","responsibilities","include","relevant","experience","seeking"]

################################################################
### Connect to DB and get all cities / endpoints for website ###
################################################################
print "Connecting..."
conn, cur = skillscout_connection_utilities.postgresql_connect() # connect to db
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
