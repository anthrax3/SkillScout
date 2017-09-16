# imports
import sys
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import FirebaseDB
from utils.skillscout_connection_utilities import PostgresqlDB
from utils.skillscout_connection_utilities import GoogleMaps

# Google Credentials and # Google maps object
oGoogleMaps = GoogleMaps()

# db object from firebase
oFirebaseDB = FirebaseDB()

# connect to postgresdb
oPostgresqlDB = PostgresqlDB()
oPostgresqlDB.execute("SELECT * FROM endpoints;", "") # get all city database
data = oPostgresqlDB.fetchall() # data is a list of tuples

# loop over all rows in endpoint data
for item in data:

    ######################################################################
    ### The key for the 'city, state' will be the google maps Place ID ###
    ######################################################################
    sCityState = item[0] + ", " + item[1]
    oGeocodeResult = oGoogleMaps.geocode(sCityState) # Geocoding the city state combo

    ###############################
    ### Begin writing operation ###
    ###############################
    sPlaceID = oGeocodeResult[0]['place_id'] # for now - assume first place ID is the 'correct' one
    oData = firebaseDataStructure(item) # Add a new city under the node name of the placeID (this is the key used by the front end)
    oFirebaseDB.childSet(sPlaceID,oData) # create a child with the name of the place id and holding the data in oData

# done with the writing; close the connection
oFirebaseDB.close()
