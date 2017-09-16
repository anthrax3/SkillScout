import sys
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import PostgresqlDB

lPositivePhrases = ["be able", "creates", "prepares", "submits", "responsible for", "provides", "conducts", "performs", "takes", "reports", "the candidate must", "the candidate will", "the employee must", "the employee will", "has to", "frequent", "processes", "you must", "you will", "inform", "develop", "focus on", "assists", "must be able to", "applications should", "does need", "are responsible for", "you will be responsible for"]
lNegativePhrases = ["we do not want", "we are not looking for", "not"]

# oPostgresqls object from util file
oPostgresql = PostgresqlDB()

# query string (seperated into multiple lines for readability, same for every city loop)
sQuery = "INSERT INTO positive_phrases (phrase) VALUES (%s) ON CONFLICT (phrase) DO NOTHING"
for i in range(0, len(lPositivePhrases)):
    # write the skill into the DB
    oPostgresql.execute(sQuery, (lPositivePhrases[i],)) # note the weird () with the , is required for psycopg2 syntax...
    print "Positive phrase data line " + str(i) + " of " + str(len(lPositivePhrases)) + " complete..."

# query string (seperated into multiple lines for readability, same for every city loop)
sQuery = "INSERT INTO negative_phrases (phrase) VALUES (%s) ON CONFLICT (phrase) DO NOTHING"
for i in range(0, len(lNegativePhrases)):
    # write the skill into the DB
    oPostgresql.execute(sQuery, (lNegativePhrases[i],)) # note the weird () with the , is required for psycopg2 syntax...
    print "Negative phrase data line " + str(i) + " of " + str(len(lNegativePhrases)) + " complete..."

# done with loop of transactions, commit them to the db
print "Commiting..."
oPostgresql.commit()
print "Done."
oPostgresql.close()
print "Connection closeed."
