'''
Custom exceptions
'''


class BadPayload(Exception):
    '''
    Exception for when modrinth rejects a sent payload
    '''
    def __init__(self, reason):
        super().__init__(reason)


# class InvalidArg(Exception):
#     '''
#     General exception raised when invalid information is given to a function
#     '''
#     def __init__(self, reason):
#         super().__init__(reason)


class ObjectInitError(Exception):
    '''
    Raised when the build function encounters unexpected or invalid data from whatever input it received
    '''
    def __init__(self, reason):
        super().__init__(reason)


class NoAccess(Exception):
    '''
    Raised when no authorization, when there was supposed to be
    '''
    def __init__(self, reason):
        super().__init__(reason)


class NotFound(Exception):
    '''
    404 Error
    '''
    def __init__(self, reason):
        super().__init__(reason)


class RateLimited(Exception):
    '''
    Self explanatory
    '''
    def __init__(self, reason):
        super().__init__(reason)


# class InvalidTimestamp(Exception):
#     '''
#     Raised when a timestamp string given isn't formatted to iso-8601
#     '''
#     def __init__(self, reason):
#         super().__init__(reason)
