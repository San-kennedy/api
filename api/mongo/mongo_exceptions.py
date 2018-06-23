"""

Generic exceptions

"""

class DbError(Exception):
    """exception when DB does not exist"""
    def __init__(self,msg):
        Exception.__init__(self,msg)

class CollectionError(Exception):
    """exception when Collection does not exist"""
    def __init__(self,msg):
        Exception.__init__(self,msg)

class ContentTypeUnsupported(Exception):
    """exception when Unsupported content type is posted"""
    def __init__(self):
        Exception.__init__(self, "Unsupported content type. Supported application JSON")

class IllegalArgumentException(Exception):
    """exception when Arguments in JSON do not meet standards"""
    def __init__(self):
        Exception.__init__(self, "illegal_argument_exception")
