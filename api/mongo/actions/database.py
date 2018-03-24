"""

Database Endpoint GET,POST and DEL


"""
import json
from datetime import datetime
import falcon
from mongo.actions.users import Users
import mongo.mongo_exceptions as custexp
from mongo.mongo_db_config import CLIENT

class Database(object):

    """
    Database Class to implement all Rest api calls
    """

    @classmethod
    def createDB(cls,database):
        """
        To create a DB, simulate Connection with required db,
        create a default collection,
        write a doc in that collection.

        Create a default user
        """
        dbs = CLIENT[database]
        coll = dbs["defaultthroughapi"]
        coll.insert_one({'db':database, "creationTimeUTC": datetime.utcnow()})
        username = database+"defaultuser"
        passwd = Users.createuser(username,database,["readWrite"])
        return {"username":username,"password":passwd,"roles":["readWrite"]}

    def on_get(self,req,res):
        """list all databases in the deployment"""
        body = CLIENT.list_database_names()
        res.body = json.dumps(body, ensure_ascii=False)
        res.status = falcon.HTTP_200

    def on_post(self,req,res):
        """Create Database"""
        try:
            if req.content_type == "application/json":
                try:
                    request = json.load(req.stream)
                    if not isinstance(request['database'], str):
                        # check for type of input
                        raise ValueError('Invalid JSON for action')
                    if (request['database'] not in CLIENT.list_database_names()):
                        userdetail = self.createDB(request['database'])
                        body = {"Database":request['database'],"userdetails":userdetail}
                        res.body = json.dumps(body, ensure_ascii=False)
                        res.status = falcon.HTTP_200
                    else:
                        raise custexp.DbError("Specified DB already exists")

                except (KeyError,ValueError):
                    raise custexp.IllegalArgumentException()

        except (Exception) as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_delete(self,req,res):
        """ delete specified databases"""
        try:
            if req.content_type == "application/json":
                try:
                    request = json.load(req.stream)
                    if not isinstance(request['database'], str):
                        # check for type of input
                        raise ValueError('Invalid JSON for action')
                    if (request['database'] in CLIENT.list_database_names()):
                        dbs = CLIENT[request['database']]
                        dbs.command("dropAllUsersFromDatabase")
                        dbs.command("dropDatabase")
                        body = {"Droppeddatabase": request['database']}
                        res.body = json.dumps(body, ensure_ascii=False)
                        res.status = falcon.HTTP_200
                    else:
                        raise custexp.DbError("Specified DB does not Exist")

                except (KeyError,ValueError):
                    raise custexp.IllegalArgumentException()

        except (Exception) as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

class DatabaseSpecific(object):
    """
    Database specific on_post

    """

    def on_get(self,req,res,database):
        """list all databases in the deployment"""
        dbs = CLIENT[database]
        body = dbs.command("dbStats")
        res.body = json.dumps(body, ensure_ascii=False)
        res.status = falcon.HTTP_200
