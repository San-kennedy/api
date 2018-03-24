"""

Shared Mongo Connection

"""


from pymongo import MongoClient


#try to fetch the below from property file
#CONNSTR = 'mongodb://host1:27017,host2:27017,host3:27017/?replicaSet=dev1'
CONNSTR = ''
USERNAME = ''
PASSWORD = ''
AUTH_DB = ''

CLIENT = MongoClient(CONNSTR, username=USERNAME, password=PASSWORD, authSource=AUTH_DB, maxPoolSize=10)
