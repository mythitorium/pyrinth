'''
objecthandler.py

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


def validate_var(vars = []):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used
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


def bulk_attr_set(object_, args, exceptions = []):
    new_args = args
    new_args.pop('self')
    print(new_args)
    for g in new_args.keys():
        if not g.lower() in exceptions:
            setattr(object_, g, new_args[g])


def build_object(): pass


def build_payload(object_):
    payload = {}

    for attr in get_members(object_):
        if isinstance(attr[1], (str, int)): # Standard
            payload[attr[0]] = attr[1]
        elif isinstance(attr[1], datetime): # Datetime
        else: # Other object
            payload[attr[0]] = build_payload(attr[1])

    return payload


def is_valid_time(time_string):
    if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T([0-9]{2}:){3}[0-9]{3}Z', time_string):
        raise InvalidTimestamp(time_string)
