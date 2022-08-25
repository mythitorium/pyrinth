'''
Separate script for universal functions utilized by classes
'''

def set_bulk_attr(target_self, input, exceptions=[]):
    '''
    Function that handles assigning mass attributes to container classes
    Updated to be less dumb
    '''
    for key in input.keys():
        if not key.lower() in exceptions:
            setattr(target_self, key, input[key])
