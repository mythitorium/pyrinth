'''
Custom exceptions
'''


class BadPayload(Exception):
    '''
    Exception for when modrinth rejects a sent payload
    '''
    def __init__(self, reason = ""):
        details = ""
        if not reason == "": details == f' ({reason})'
        super().__init__(f'Sent invalid or unusable data{details}')


class ArgError(Exception):
    '''
    General exception raised when invalid information is given to a function
    '''
    def __init__(self, index, actual_type, target_type, is_nested = False, nested_index = 0):
        if not is_nested:
            super().__init__(f"At arg {index}: Expected {target_type}, got {actual_type}")
        else:
            super().__init__(f"At index {nested_index} at {list} arg {index}: Expected {target_type}, got {actual_type}")


class NoAccess(Exception):
    '''
    Raised when no authorization, when there was supposed to be
    '''
    def __init__(self, reason, more_reasons = ""):
        if more_reasons == "":
            details = ""
        else:
            details = f' ({more_reasons})'
        
        super().__init__(f'{reason.capitalize()}; Valid authorization required{details}')


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


class InvalidTimestamp(Exception):
    '''
    Raised when a timestamp string given isn't formatted to iso-8601
    '''
    def __init__(self, time_string):
        super().__init__(f'{time_string} must be of iso format')
