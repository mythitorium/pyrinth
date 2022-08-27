'''
Custom exceptions
'''


class BadPayload(Exception):
    '''
    Exception for when modrinth rejects a sent payload
    '''
    def __init__(self):
        super().__init__(f'Sent invalid or unusable data')


class ArgError(Exception):
    '''
    General exception raised when invalid information is given to a function
    '''
    def __init__(self, index, actual_type, target_type):
        super().__init__(f"At arg {index}: Expected {target_type}, got {actual_type}")


class NoAccess(Exception):
    '''
    Raised when no authorization, when there was supposed to be
    '''
    def __init__(self):
        super().__init__(f'Valid authorization required')


class NotFound(Exception):
    '''
    404 Error
    '''
    def __init__(self, id, target):
        super().__init__(f"Getting {target.capitalize()} '{id}' returned nothing")


class RateLimited(Exception):
    '''
    Self explanatory
    '''
    def __init__(self, cooldown):
        self.cooldown = cooldown
        super().__init__(f'Too many requests. Window reset in {cooldown:.2f} seconds')
