'''
handler.py

this acts as a mini-module which validates the contents of arguments and objects
'''


# def old_validate_object(objects, expected_type):
#     '''
#     Used to validate the arguments for functions. Catches bad data before it's used
# 
#     Version 3
#     '''
#     for obj in objects:
#         # Check
#         if not isinstance(obj, expected_type):
#             raise TypeError(f'Invalid type: expected {expected_type}, got {type(obj)}')



def validate_objects(object_table):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used
    Version 4

    Expected format:
    {
        tag : (object, expected_type)
    }
    '''
    for item in object_table:
        obj = object_table[item][0]
        expected_type = object_table[item][1]
        if not isinstance(obj, expected_type):
            raise TypeError(f'Invalid type: with {item}; expected {expected_type}, got {type(obj)}')
