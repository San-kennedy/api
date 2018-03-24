"""

Generic exceptions

"""

class DbError(Exception):
    """exception when DB does not exist"""
    def __init__(self,msg):
        Exception.__init__(self,msg)

class CollectionError(Exception):
    """exception when DB does not exist"""
    def __init__(self,msg):
        Exception.__init__(self,msg)

class ContentTypeUnsupported(Exception):
    """exception when DB does not exist"""
    def __init__(self):
        Exception.__init__(self, "Unsupported content type. Supported application JSON")

class IllegalArgumentException(Exception):
    """exception when DB does not exist"""
    def __init__(self):
        Exception.__init__(self, "illegal_argument_exception")
