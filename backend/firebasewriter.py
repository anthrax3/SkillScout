# imports
import psycopg2
import googlemaps
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# declare vars
gmaps = googlemaps.Client(key='AIzaSyDnc2gf9n0QcR4mBiM9SBrbL1e3oJWAvzI')

################################################################
### Connect to DB and get all cities / endpoints for website ###
################################################################
conn = psycopg2.connect("dbname=test user=postgres") # connect to db
cur = conn.cursor() # Open a cursor to perform database operations
cur.execute("SELECT * FROM website_endpoints;") # get all city database
data = cur.fetchall() # data is a list of tuples

for item in data:

    #############################################################
    ### The key for the city will be the google maps Place ID ###
    #############################################################

    # Geocoding an address
    oGeocodeResult = gmaps.geocode(item[0]) # first item is city name
    sPlaceID = oGeocodeResult['results']['place_id']

    ###############################
    ### Begin writing operation ###
    ###############################

    # authenticate
    cred = credentials.Certificate('SkillScout-c76bf4dc2bfa.json')
    default_app = firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://skillscout-123.firebaseio.com/'
    })

    # get the root of the db
    root = db.reference()

    # just screwing around - delete the node first
    root.child(sPlaceID).delete()

    # Add a new city under /newTest
    root.child(sPlaceID).push({
        "test" : {
        "doughnutChartData" : {
          "datasets" : [ {
            "backgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#52acdd" ],
            "data" : [ 30, 20, 40, 10 ],
            "hoverBackgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#52acdd" ]
          } ],
          "labels" : [ "Engineering", "Human Resources", "Information Technology", "Sciences" ]
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
          "jobsTotal" : item[1], # second item - jobs total
          "jobsYesterday" : item[2], # second item - jobs total
          "leadDescription" : item[3], # second item - jobs total
          "leadDescriptionCount" : item[4], # second item - jobs total
          "leadDescriptionPerc" : item[5], # second item - jobs total
          "leadSkill" : item[6], # second item - jobs total
          "leadSkillCount" : item[7], # second item - jobs total
          "leadSkillPerc" : item[8], # second item - jobs total
          "percChangeMonth" : item[9], # second item - jobs total
          "percChangeYear" : item[10] # second item - jobs total
        }
      }
    })
