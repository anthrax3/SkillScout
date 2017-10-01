import sys
import pandas as pd
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import PostgresqlDB

sCity = "San Francisco"
sState = "California"

print "Connecting..."
oPostgresql = PostgresqlDB() # db object
print "Done."

# get all job titles for the given city/state
sQuery = "SELECT title, docid FROM job_skills WHERE city = '" + sCity.lower() + "' AND state = '" + sState.lower() + "';"
oPostgresql.execute(sQuery, "")
tTitlesDocid = oPostgresql.fetchall()

# convert tuples to sepeate lists
lTitles = [i[0] for i in tTitlesDocid]
lDocids = [i[1] for i in tTitlesDocid]


# lookup industry from title - if it is not found, log it out
for sTitle in lTitles:
    sTitle = sTitle.replace("'", "") # escape characters
    print(sTitle)
    sQuery = "SELECT industry FROM title_industry_map WHERE title = '" + sTitle.lower() + "';"
    oPostgresql.execute(sQuery, "")
    lIndustry = oPostgresql.fetchone()
    if not lIndustry:
        print "No industry found for job title " + sTitle.lower() + "!"
        print "You can add it to the db with:"
        print "INSERT INTO title_industry_map (title, industry) VALUES ('" + sTitle.lower() + "', <<correct industry here>>);"
        print ""
        print ""


# write that all that back to the job_skills table (use the docid as key of course to make sure we are setting correct job)
for i in range(0, len(lTitles)):
    sTitle = lTitles[i].lower()
    sTitle = sTitle.replace("'", "") # escape characters
    sQuery = "UPDATE job_skills SET industry = '" + sTitle + "' WHERE docid = " + str(lDocids[i]) + ";"
    oPostgresql.execute(sQuery, "")
oPostgresql.commit()

# get all industries from this city/state, now that they have been written
sQuery = "SELECT industry FROM job_skills WHERE city = '" + sCity.lower() + "' AND state = '" + sState.lower() + "';"
oPostgresql.execute(sQuery, "")
tIndustries = oPostgresql.fetchall()

# for each industry, get sums and write to endpoints table

# convert tuple to list
lIndustries = [i[0] for i in tIndustries]

for sIndustry in lIndustries:
    sQuery = "SELECT * FROM job_skills WHERE city = '" + sCity.lower() + "' AND state = '" + sState.lower() + "' AND industry = '" + sIndustry + "';"
    oPostgresql.execute(sQuery, "")
    lJobSkills = oPostgresql.fetchall() # array
    lSkillTimesPairs = [] # initialize the skill/times pair list
    for i in range(0, len(lJobSkills)):
        lSkillTimesPairs.extend([{'skill': lJobSkills[i][5], 'times': lJobSkills[i][6]},
        {'skill': lJobSkills[i][7], 'times': lJobSkills[i][8]},
        {'skill': lJobSkills[i][9], 'times': lJobSkills[i][10]},
        {'skill': lJobSkills[i][11], 'times': lJobSkills[i][12]},
        {'skill': lJobSkills[i][13], 'times': lJobSkills[i][14]},
        {'skill': lJobSkills[i][15], 'times': lJobSkills[i][16]},
        {'skill': lJobSkills[i][17], 'times': lJobSkills[i][18]},
        {'skill': lJobSkills[i][19], 'times': lJobSkills[i][20]},
        {'skill': lJobSkills[i][21], 'times': lJobSkills[i][22]},
        {'skill': lJobSkills[i][23], 'times': lJobSkills[i][24]}])

    #make global sum from the
    df = pd.DataFrame(lSkillTimesPairs)
    df = df.groupby('skill').sum() # sum of times accross all skills
    df = df.dropna() # remove any NA values
    df = df.sort_values(by='times',ascending=False) # sort descending

    # convert dataframe to json
    sJSON = df.to_json()

    # take only top 10 (if not even 10, )
    tValues = (sCity.lower(), sState.lower(), sIndustry.lower(), sJSON.lower())
    print(sJSON.lower())
    sQuery = "INSERT INTO industry_skills VALUES (%s,%s,%s,%s) ON CONFLICT (city, state, industry) DO UPDATE SET skill_times_json = '" + sJSON.lower() + "'; "
    oPostgresql.execute(sQuery, tValues)
    oPostgresql.commit()

# close connection
oPostgresql.close()
