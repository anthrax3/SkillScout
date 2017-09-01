import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# authenticate
cred = credentials.Certificate('SkillScout-c76bf4dc2bfa.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://skillscout-123.firebaseio.com/'
})

# get the root of the db
root = db.reference()

# just screwing around - delete the node first
root.child('newTest').delete()

# Add a new city under /newTest
# root.child('newTest').push({
#     "test" : {
#     "doughnutChartData" : {
#       "datasets" : [ {
#         "backgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#52acdd" ],
#         "data" : [ 30, 20, 40, 10 ],
#         "hoverBackgroundColor" : [ "#FF6384", "#36A2EB", "#FFCE56", "#74f442", "#52acdd" ]
#       } ],
#       "labels" : [ "Engineering", "Human Resources", "Information Technology", "Sciences" ]
#     },
#     "longTrendsChartData" : {
#       "datasets" : [ {
#         "backgroundColor" : "rgba(75,192,192,0.4)",
#         "borderCapStyle" : "butt",
#         "borderColor" : "rgba(75,192,192,1)",
#         "borderDashOffset" : 0,
#         "borderJoinStyle" : "miter",
#         "data" : [ 45, 32, 33, 35, 30 ],
#         "fill" : False,
#         "label" : "",
#         "lineTension" : 0.1,
#         "pointBackgroundColor" : "#fff",
#         "pointBorderColor" : "rgba(75,192,192,1)",
#         "pointBorderWidth" : 1,
#         "pointHitRadius" : 10,
#         "pointHoverBackgroundColor" : "rgba(75,192,192,1)",
#         "pointHoverBorderColor" : "rgba(220,220,220,1)",
#         "pointHoverBorderWidth" : 2,
#         "pointHoverRadius" : 5,
#         "pointRadius" : 1
#       } ],
#       "labels" : [ "June", "July", "August", "September", "October" ]
#     },
#     "recentTrendsChartData" : {
#       "datasets" : [ {
#         "backgroundColor" : "rgba(75,192,192,0.4)",
#         "borderCapStyle" : "butt",
#         "borderColor" : "rgba(75,192,192,1)",
#         "borderDashOffset" : 0,
#         "borderJoinStyle" : "miter",
#         "data" : [ 30, 32, 33, 35, 45 ],
#         "fill" : False,
#         "label" : "",
#         "lineTension" : 0.1,
#         "pointBackgroundColor" : "#fff",
#         "pointBorderColor" : "rgba(75,192,192,1)",
#         "pointBorderWidth" : 1,
#         "pointHitRadius" : 10,
#         "pointHoverBackgroundColor" : "rgba(75,192,192,1)",
#         "pointHoverBorderColor" : "rgba(220,220,220,1)",
#         "pointHoverBorderWidth" : 2,
#         "pointHoverRadius" : 5,
#         "pointRadius" : 1
#       } ],
#       "labels" : [ "January", "February", "March", "April", "May" ]
#     },
#     "writtenDescriptionData" : {
#       "leadDescription" : "Developer",
#       "leadSkill" : "Webscraping",
#       "leadSkillPerc" : 23,
#       "percChangeMonth" : -5
#     }
#   }
# })
