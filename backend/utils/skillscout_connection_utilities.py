import psycopg2
import re
import os
import pymongo
from pymongo import MongoClient
import googlemaps
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from os.path import expanduser
from bs4 import BeautifulSoup
from sshtunnel import SSHTunnelForwarder

##################################################
### This module includes useful definitions    ###
### for various utilities which are used in    ###
### many places accross the skillscout backend ###
##################################################

class LocalPostgresqlDB(object):
    server = None
    conn = None
    cur = None

    def __init__(self):
        # server settings
        SERVER_HOST = os.environ.get("SERVER_HOST")
        SERVER_PORT = str(os.environ.get("SERVER_PORT"))
        SERVER_DB_PORT = str(os.environ.get("SERVER_DB_PORT"))
        SERVER_USER = os.environ.get("SERVER_USER")
        SERVER_PASSWORD = os.environ.get("SERVER_PASSWORD")
        # db settings
        DB_NAME = os.environ.get("PRIVATE_SKILLSCOUT_DB_NAME")
        DB_USER = os.environ.get("PRIVATE_SKILLSCOUT_DB_USER")
        DB_PASSWORD = os.environ.get("PRIVATE_SKILLSCOUT_DB_PASSWORD")
        DB_HOST = os.environ.get("PRIVATE_SKILLSCOUT_DB_HOST")
        DB_PORT = os.environ.get("PRIVATE_SKILLSCOUT_DB_PORT")
        self.server = SSHTunnelForwarder(
            (SERVER_HOST, int(SERVER_PORT)),
            ssh_username=SERVER_USER,
            ssh_password=SERVER_PASSWORD,
            remote_bind_address=('127.0.0.1', int(SERVER_DB_PORT)),
            local_bind_address=('127.0.0.1', int(DB_PORT))
        )
        self.server.start()
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.cur = self.conn.cursor()

    def execute(self, query, params):
        return self.cur.execute(query, params)

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()

    def __del__(self):
        self.conn.close()
        self.server.stop()

class PostgresqlDB(object):
    conn = None
    cur = None

    def __init__(self):
        DB_NAME = os.environ.get("SKILLSCOUT_DB_NAME")
        DB_USER = os.environ.get("SKILLSCOUT_DB_USER")
        DB_PASSWORD = os.environ.get("SKILLSCOUT_DB_PASSWORD")
        DB_HOST = os.environ.get("SKILLSCOUT_DB_HOST")
        DB_PORT = os.environ.get("SKILLSCOUT_DB_PORT")
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.cur = self.conn.cursor()

    def execute(self, query, params):
        return self.cur.execute(query, params)

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()

    def __del__(self):
        self.conn.close()

class FirebaseDB(object):
    app = None
    root = None

    def __init__(self):
        sCredPath = expanduser("~") + '/SkillScout-c76bf4dc2bfa.json' # path to root, regardless of OS
        cred = credentials.Certificate(sCredPath) # authenticate
        print "Connecting to Firebase Realtime DB..."
        self.app = firebase_admin.initialize_app(cred, {
            'databaseURL' : 'https://skillscout-123.firebaseio.com/'
        })
        self.root = db.reference() # get the root of the db (we do all our inserting here)

    def childSet(self, childName, oData):
        return self.root.child(childName).set(oData)

    def close():
        return firebase_admin.delete_app(self.app)

    def __del__(self):
        self.conn.close()

class GoogleMaps(object):
    gmaps = None
    #####################################
    ### Connect to google maps client ###
    #####################################
    def __init__(self):
        SKILLSCOUT_GOOGLE_GEOCODING_KEY = os.environ.get("SKILLSCOUT_GOOGLE_GEOCODING_KEY")
        self.gmaps = googlemaps.Client(key=SKILLSCOUT_GOOGLE_GEOCODING_KEY)

    def geocode(location):
        return self.gmaps.geocode(location)

def firebaseDataStructure(item):
    ##########################################################################
    ### To keep main code clean, the firesbase data structure is kept here ###
    ##########################################################################
    return { "city": item[0],
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
      }

def cleanHTML(sHTML):
    sHTML = sHTML.replace("<li>", "") # for now, this is a way to convert lists to sentances
    sHTML = sHTML.replace("</li>", ".")
    oSoup = BeautifulSoup(sHTML, "html5lib") # BeautifulSoup the html!
    [s.extract() for s in oSoup('head')] # remove everything in <head> tag
    [s.extract() for s in oSoup('script')] # remove everything in <script> tags
    [s.extract() for s in oSoup('noscript')] # remove everything in <noscript> tags
    sText = oSoup.text # get raw text left in article
    sText.lower() # convert any uppercase letters to lowercase
    sText = re.sub(r'\s+', ' ', sText) # clean up all the leftover whitespace with just a single space
    sText = sText.encode('utf-8')
    return sText
