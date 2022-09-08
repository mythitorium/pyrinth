'''
handler.py

this acts as a mini-module which validates the contents of arguments and objects
'''

def validate_object(objects, expected_type):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used

    Version 3
    '''
    for obj in objects:
        # Check
        if not isinstance(obj, expected_type):
            raise InvalidValue(f'Invalid type: expected {expected_type}, got {type(obj)}')
