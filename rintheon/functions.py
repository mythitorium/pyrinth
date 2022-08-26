'''
Separate script for useful functions
'''

from .errors import *

def set_bulk_attr(caller, input, exceptions=[]):
    '''
    Function that handles assigning mass attributes to container classes
    Updated to be less dumb
    '''
    for key in input.keys():
        if not key.lower() in exceptions:
            setattr(caller, key, input[key])


def validate_args(args: list, types: list):
    for index in range(len(args)):
        if not type(args[index]) == types[index]:
            raise InputError(index, type(args[index]), types[index])

