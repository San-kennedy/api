"""
Main module to launch APIs
"""

import falcon
from mongo.actions.users import Users
import mongo.actions.database as db
from mongo.actions.collection import Collection

API = falcon.API()

MONGO_USERS = Users()
MONGO_DATABASES = db.Database()
MONGO_SPECIFIC_DB = db.DatabaseSpecific()
MONGO_COLLECTION = Collection()

API.add_route('/mongo/database', MONGO_DATABASES)
API.add_route('/mongo/{database}', MONGO_SPECIFIC_DB)
API.add_route('/mongo/{database}/collection', MONGO_COLLECTION)
API.add_route('/mongo/{database}/users', MONGO_USERS)
