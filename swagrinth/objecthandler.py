'''
objecthandler.py

this acts as a mini-module which
- validates the contents of arguments and objects
- converts objects and data into valid payloads to be sent
- handles applying attributes to classes

OBJECT VALIDATION FORMATTING

# To do

VARIABLE VALIDATION FORMATTING

[
    (target_var, expected_type, expected_nested_type)
]
'''


def validate_args(args: list, types: list):
    '''
    Used to validate the arguments for functions. Catches bad data before it's used

    NOTE: DEPRECIATED
    '''
    for index in range(len(args)):
        if not type(args[index]) == types[index]:
            raise ArgError(index, type(args[index]), types[index])


def validate_var(vars):
    count = 0
    for var in vars:
        # Check
        if not type(var[0]) == var[1]:
            raise ArgError(count, type(var[0]), var[1])
        
        # Check indexes if array
        if type(var[0]) == list:
            list_count = 0
            for item in var[0]:
                if not type(item) == var[2]:
                    raise ArgError(count, type(item), var[2], True, list_count)
                list_count += 1
        
        # Increase count
        count += 1


def bulk_attr_set(object_, exceptions = []):
    args = object_.locals()
    for g in args.keys():
        if not g.lower() in exceptions:
            setattr(object_, g, args[g])
