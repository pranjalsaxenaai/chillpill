# filepath: /c:/code/chillpill/api/test_settings.py
from .settings import *

# Override the database settings for testing with mongomock
from mongoengine import disconnect, connect
import mongomock

# Disconnect any existing connections
disconnect()

# Connect to the mock MongoDB instance provided by mongomock
connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)