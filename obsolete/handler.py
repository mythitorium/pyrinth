'''
handler.py

this acts as a mini-module which validates the contents of arguments and objects

OBJECT VALIDATION FORMATTING

# To do

VARIABLE VALIDATION FORMATTING

[
    (target_var, expected_type, expected_nested_type)
]
'''

from inspect import *
from datetime import *
import re
from .errors import *


def validate_vars(vars = []):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used
    NOTE: Obsolete 
    '''
    count = 0
    for var in vars:
        # Check
        if not type(var[0]) == var[1]:
            raise InvalidArg(count, type(var[0]), var[1])
        
        # Check indexes if array
        if type(var[0]) == list:
            list_count = 0
            for item in var[0]:
                if not type(item) == var[2]:
                    raise InvalidArg(count, type(item), var[2], True, list_count)
                list_count += 1
        
        # Increase count
        count += 1


def validate_object(objects, expected_type):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used

    Version 3
    '''
    for obj in objects:
        # Check
        if not isinstance(obj, expected_type):
            raise InvalidValue(f'Invalid type: expected {expected_type}, got {type(obj)}')


def bulk_attr_set(object_, args, exceptions = []):
    '''
    NOTE: Obsolete
    '''
    new_args = args
    new_args.pop('self')
    print(new_args)
    for g in new_args.keys():
        if not g.lower() in exceptions:
            setattr(object_, g, new_args[g])


def build_payload(object_):
    payload = {}

    for attr in get_members(object_):
        if isinstance(attr[1], (str, int)): # Standard
            payload[attr[0]] = attr[1]
        elif isinstance(attr[1], datetime): # Datetime
            pass
        else: # Other object
            payload[attr[0]] = build_payload(attr[1])

    return payload


def is_valid_time(time_string):
    print(time_string)
    if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T([0-9]{2}:){2}[0-9]{2}.[0-9]{3,}Z', time_string):
        raise InvalidTimestamp(f'{time_string} is not a valid iso timestamp')
