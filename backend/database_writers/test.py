import sys
import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import LocalPostgresqlDB

oLocalPostgresql = LocalPostgresqlDB() # remote, non-heroku db connect

oLocalPostgresql.execute("SELECT * FROM test;", "")
print oLocalPostgresql.fetchall()

# SERVER_HOST = os.environ.get("SERVER_HOST")
# SERVER_PORT = str(os.environ.get("SERVER_PORT"))
# SERVER_USER = os.environ.get("SERVER_USER")
# SERVER_PASSWORD = os.environ.get("SERVER_PASSWORD")
# # db settings
# DB_NAME = os.environ.get("PRIVATE_SKILLSCOUT_DB_NAME")
# DB_USER = os.environ.get("PRIVATE_SKILLSCOUT_DB_USER")
# DB_PASSWORD = os.environ.get("PRIVATE_SKILLSCOUT_DB_PASSWORD")
# DB_HOST = os.environ.get("PRIVATE_SKILLSCOUT_DB_HOST")
# DB_PORT = os.environ.get("PRIVATE_SKILLSCOUT_DB_PORT")
# server = SSHTunnelForwarder(
#     (SERVER_HOST, int(SERVER_PORT)),
#     ssh_username=SERVER_USER,
#     ssh_password=SERVER_PASSWORD,
#     remote_bind_address=('127.0.0.1', 5432),
#     local_bind_address=('127.0.0.1',2345)
# )
# server.start()
