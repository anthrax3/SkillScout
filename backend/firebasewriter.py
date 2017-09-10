# imports
import os
from os.path import expanduser
import psycopg2
import googlemaps
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# DB Credentials (in .bashrc)
DB_NAME = os.environ.get("SKILLSCOUT_DB_NAME")
DB_USER = os.environ.get("SKILLSCOUT_DB_USER")
DB_PASSWORD = os.environ.get("SKILLSCOUT_DB_PASSWORD")
DB_HOST = os.environ.get("SKILLSCOUT_DB_HOST")
DB_PORT = os.environ.get("SKILLSCOUT_DB_PORT")

# Google Credentials (in .bashrc)
SKILLSCOUT_GOOGLE_GEOCODING_KEY = os.environ.get("SKILLSCOUT_GOOGLE_GEOCODING_KEY")

# Google maps object
gmaps = googlemaps.Client(key=SKILLSCOUT_GOOGLE_GEOCODING_KEY)

##############################
### Connect to firebase DB ###
##############################
sCredPath = expanduser("~") + '/SkillScout-c76bf4dc2bfa.json' # path to root, regardless of OS
cred = credentials.Certificate(sCredPath) # authenticate
app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://skillscout-123.firebaseio.com/'
})
root = db.reference() # get the root of the db (we do all our inserting here)

################################################################
### Connect to DB and get all cities / endpoints for website ###
################################################################
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) # connect to db
print "Connecting..."
cur = conn.cursor() # Open a cursor to perform database operations
print "Done."
cur.execute("SELECT * FROM endpoints;") # get all city database
data = cur.fetchall() # data is a list of tuples
#data = cur.fetchone() # for testing purposes, just the first row
for item in data:

    ######################################################################
    ### The key for the 'city, state' will be the google maps Place ID ###
    ######################################################################
    sCityState = item[0] + ", " + item[1]
    # Geocoding an address
    oGeocodeResult = gmaps.geocode(sCityState) # first item is city name
    sPlaceID = oGeocodeResult[0]['place_id'] # for now - assume first place ID is the 'correct' one

    ###############################
    ### Begin writing operation ###
    ###############################
    # Add a new city under the node name of the placeID (this is the key used by the front end)
    root.child(sPlaceID).set({
        "city": item[0],
        "doughnutChartData" : {
          "datasets" : [ {
            "backgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#d142f4" ],
            "data" : [ item[13], item[15], item[17], item[19], item[21] ],
            "hoverBackgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#d142f4" ]
          } ],
          "labels" : [ item[12], item[14], item[16], item[18], item[20] ]
        },
        "longTrendsChartData" : {
          "datasets" : [ {
            "backgroundColor" : "rgba(75,192,192,0.4)",
            "borderCapStyle" : "butt",
            "borderColor" : "rgba(75,192,192,1)",
            "borderDashOffset" : 0,
            "borderJoinStyle" : "miter",
            "data" : [ {
              "x" : 0,
              "y" : 10
            }, {
              "x" : 2,
              "y" : 23
            }, {
              "x" : 4,
              "y" : 24
            }, {
              "x" : 6,
              "y" : 50
            }, {
              "x" : 8,
              "y" : 75
            } ],
            "fill" : False,
            "label" : "",
            "lineTension" : 0,
            "pointBackgroundColor" : "#fff",
            "pointBorderColor" : "rgba(75,192,192,1)",
            "pointBorderWidth" : 1,
            "pointHitRadius" : 10,
            "pointHoverBackgroundColor" : "rgba(75,192,192,1)",
            "pointHoverBorderColor" : "rgba(220,220,220,1)",
            "pointHoverBorderWidth" : 2,
            "pointHoverRadius" : 5,
            "pointRadius" : 1
          } ],
          "labels" : [ "1 year ago", "10 months ago", "8 months ago", "6 months ago", "4 months ago" ]
        },
        "recentTrendsChartData" : {
          "datasets" : [ {
            "backgroundColor" : "rgba(75,192,192,0.4)",
            "borderCapStyle" : "butt",
            "borderColor" : "rgba(75,192,192,1)",
            "borderDashOffset" : 0,
            "borderJoinStyle" : "miter",
            "data" : [ {
              "x" : 0,
              "y" : 15
            }, {
              "x" : 8,
              "y" : 45
            }, {
              "x" : 10,
              "y" : 50
            }, {
              "x" : 11,
              "y" : 89
            }, {
              "x" : 12,
              "y" : 99
            } ],
            "fill" : False,
            "label" : "",
            "lineTension" : 0,
            "pointBackgroundColor" : "#fff",
            "pointBorderColor" : "rgba(75,192,192,1)",
            "pointBorderWidth" : 1,
            "pointHitRadius" : 10,
            "pointHoverBackgroundColor" : "rgba(75,192,192,1)",
            "pointHoverBorderColor" : "rgba(220,220,220,1)",
            "pointHoverBorderWidth" : 2,
            "pointHoverRadius" : 5,
            "pointRadius" : 1
          } ],
          "labels" : [ "3 months ago", "2 weeks ago", "2 weeks ago", "last week", "today" ]
        },
        "writtenDescriptionData" : {
          "jobsTotal" : item[2], # third item - jobs total
          "jobsYesterday" : item[3], # fourth item - jobs total
          "leadDescription" : item[4], # etc.- jobs total
          "leadDescriptionCount" : item[5], # etc.- jobs total
          "leadDescriptionPerc" : item[6], # etc.- jobs total
          "leadSkill" : item[7], # etc.- jobs total
          "leadSkillCount" : item[8], # etc.- jobs total
          "leadSkillPerc" : item[9], # etc.- jobs total
          "percChangeMonth" : item[10], # etc.- jobs total
          "percChangeYear" : item[11] # etc.- jobs total
        }
      })

# done with the writing; close the connection
firebase_admin.delete_app(app)
