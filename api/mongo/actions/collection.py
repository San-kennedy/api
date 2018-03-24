"""

Implement RestAPI for collection object

"""

import json
import falcon
from mongo.mongo_db_config import CLIENT
import mongo.mongo_exceptions as custexp


class Collection(object):
    """
    Class to implement get,post,put and delete

    """
    @classmethod
    def checkDb(cls, database):
        if database not in CLIENT.list_database_names():
            raise custexp.DbError("Database doesn't exist")
        else:
            return True

    def on_get(self, req, res, database):
        """ GET functionality"""
        try:
            if self.checkDb(database):
                #GO feth the collections in Db and respond 200OK
                dbs = CLIENT[database]
                body = dbs.collection_names()
                res.body = json.dumps(body, ensure_ascii=False)
                res.status = falcon.HTTP_200

        except custexp.DbError as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_post(self, req, res, database):
        """ POST functionality"""
        try:
            if self.checkDb(database):
                if req.content_type == "application/json":
                    try:
                        request = json.load(req.stream)
                        if ((not isinstance(request['collection'], str)) or (not isinstance(request['capped'], bool))):
                            # JSON field validation
                            raise custexp.IllegalArgumentException()
                        dbs = CLIENT[database]
                        if request['capped']:
                            if not isinstance(request['size'], int):
                                raise ValueError('Expecting integer for size')
                                #create capped collection based on maxPoolSize
                            dbs.create_collection(request['collection'], capped=True, size=request['size'])
                            body = {"CreatedCollection":request['collection'], "cappedsize": request['size']}

                        else:
                            dbs.create_collection(request['collection'])
                            body = {"CreatedCollection":request['collection'], "capped": False}

                        res.body = json.dumps(body,ensure_ascii=False)
                        res.status = falcon.HTTP_200

                    except (KeyError, ValueError):
                        raise custexp.IllegalArgumentException()
                else:
                    raise custexp.ContentTypeUnsupported()
        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body,ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_delete(self, req, res, database):
        """Delete functionality"""
        try:
            if self.checkDb(database):
                if req.content_type == "application/json":
                    request = json.load(req.stream)
                    if not isinstance(request['collection'],str):
                        raise custexp.IllegalArgumentException()
                    dbs = CLIENT[database]
                    if request['collection'] not in dbs.collection_names():
                        raise custexp.CollectionError("Collection does not exist")
                    dbs.drop_collection(request['collection'])
                    body = {"DroppedCollection":request['collection']}
                    res.body = json.dumps(body,ensure_ascii=False)
                    res.status = falcon.HTTP_200

                else:
                    raise custexp.ContentTypeUnsupported()
        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body,ensure_ascii=False)
            res.status = falcon.HTTP_400
