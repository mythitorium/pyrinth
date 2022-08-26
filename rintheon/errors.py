'''
Custom exceptions
'''


class BadPayload(Exception):
    pass


class InputError(Exception):
    def __init__(self, index, actual_type, target_type):
        super().__init__(f"At arg {index}: Expected {target_type}, got {actual_type}")


class NoAccess(Exception):
    pass


class NotFound(Exception):
    def __init__(self, id, target):
        super().__init__(f"404: {target.capitalize()} '{id}' not found")


class RateLimited(Exception):
    def __init__(self, cooldown):
        self.cooldown = cooldown
        super().__init__(f'Too many requests. Window reset in {cooldown:.2f} seconds')