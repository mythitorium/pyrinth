'''
Base class lol
'''

class BaseClass:
    '''
    Parent class all other container classes inherit from
    '''

    def set_bulk_attr(self, caller, input, exceptions=[]):
        '''
        Function that handles assigning mass attributes to container classes
        Updated to be less dumb
        '''
        for key in input.keys():
            if not key.lower() in exceptions:
                setattr(caller, key, input[key])