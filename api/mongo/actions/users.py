"""

Users Endpoint GET,POST,PUT,DEL


"""
import json
import secrets
import falcon
import mongo.mongo_exceptions as custexp
from mongo.mongo_db_config import CLIENT

class Users(object):
    """
    Users Class to implement all Rest api calls

    """

    @classmethod
    def check_db(cls, db_to_check):
        """check if the requested DB is valid"""
        if db_to_check not in CLIENT.list_database_names():
            raise custexp.DbError("DB does not exist")
        else:
            return True

    @classmethod
    def fetchusers(cls, database):
        """snippet to fetchusers from DB"""
        dbs = CLIENT.admin
        coll = dbs['system.users']
        result = coll.find({'db': database}, projection={'user':True, 'roles':True, '_id':False})
        doc = []
        for i in result:
            doc.append(i)
        return doc

    @classmethod
    def createuser(cls, username, database, roles):
        """snippet to create user"""
        dbs = CLIENT[database]
        passwd = secrets.token_urlsafe(8)
        dbs.command("createUser", username, pwd=passwd, roles=roles)
        return passwd

    @classmethod
    def updateuserpassword(cls, username, database):
        """snippet to update user password"""
        dbs = CLIENT[database]
        passwd = secrets.token_urlsafe(8)
        dbs.command("updateUser", username, pwd=passwd)
        return passwd

    @classmethod
    def updateuserrole(cls, username, database, roles):
        """updateUser roles"""
        dbs = CLIENT[database]
        dbs.command("updateUser", username, roles=roles)

    @classmethod
    def deleteuser(cls, username, database):
        """snippet to delete user"""
        dbs = CLIENT[database]
        dbs.command("dropUser", username)

    # on get functionality
    def on_get(self, req, res, database):
        """on get functionality"""
        try:
            if self.check_db(database):
                doc = self.fetchusers(database)
                res.body = json.dumps(doc, ensure_ascii=False)
                res.status = falcon.HTTP_200

        except custexp.DbError as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

    # on post functionality

    def on_post(self, req, res, database):
        """on post functionality"""
        try:
            if self.check_db(database):
                if req.content_type == "application/json":
                    try:
                        request = json.load(req.stream)
                        if ((not isinstance(request['username'], str)) or (not isinstance(request['roles'], list))):
                            # check the type of values provided as input
                            # username must an instance of string
                            # roles must be an instance of list
                            raise ValueError('Invalid JSON for action')
                        passwd = self.createuser(request['username'], database, request['roles'])
                        response = {'username':request['username'], 'password':passwd, 'roles':request['roles']}
                        res.body = json.dumps(response, ensure_ascii=False)
                        res.status = falcon.HTTP_200

                    except (KeyError, ValueError):
                        raise custexp.IllegalArgumentException()
                else:
                    raise custexp.ContentTypeUnsupported()

        except (Exception) as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_put(self, req, res, database):
        """on put functionality"""
        try:
            if self.check_db(database):
                if req.content_type == "application/json":
                    try:
                        request = json.load(req.stream)
                        if ((not isinstance(request['username'], str)) or (not isinstance(request['roles'], list)) or \
                                (not isinstance(request['password'], bool))):
                            # check the type of values provided as input
                            # username must an instance of string,
                            # roles must be an instance of list, password must be a bool
                            raise ValueError()
                        if request['password']:
                            #when password reset is required
                            if not request['roles']:
                                #when the roles list is empty, intent is to just change password
                                passwd = self.updateuserpassword(request['username'], database)
                                response = {'username':request['username'], 'password': passwd}
                            else:
                                #intent is to change password and roles
                                passwd = self.updateuserpassword(request['username'], database)
                                self.updateuserrole(request['username'], database, request['roles'])
                                response = {'username':request['username'], 'password': passwd, 'roles':request['roles']}
                        else:
                            # when password reset is not true intent is to just change the roles
                            if request['roles']:
                                self.updateuserrole(request['username'], database, request['roles'])
                                response = {'username':request['username'], 'roles':request['roles']}
                            else:
                                raise Exception('Trying to revoke all roles from user, Please delete user instead')

                        res.body = json.dumps(response, ensure_ascii=False)
                        res.status = falcon.HTTP_200

                    except (KeyError, ValueError):
                        raise custexp.IllegalArgumentException()
                else:
                    raise custexp.ContentTypeUnsupported()

        except (Exception) as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_delete(self, req, res, database):
        """actions on delete"""
        try:
            if self.check_db(database):
                if req.content_type == "application/json":
                    try:
                        request = json.load(req.stream)
                        if not isinstance(request['username'], str):
                            # check the type of values provided as input
                            raise ValueError()
                        self.deleteuser(request['username'], database)
                        doc = {"deletedUser":request['username']}
                        res.body = json.dumps(doc, ensure_ascii=False)
                        res.status = falcon.HTTP_200

                    except (KeyError, ValueError):
                        raise custexp.IllegalArgumentException()
                else:
                    raise custexp.ContentTypeUnsupported()

        except (Exception) as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400
