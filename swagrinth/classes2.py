'''
Data classes
'''

from datetime import datetime
from .handler import *
from inspect import isclass
from .formatting import *
from .errors import *
import copy


class BaseObject():
    '''
    Base class all other data container classes inherit from
    '''

    def _build(self, input_data: dict, blueprint_plan: dict, corrections = {}):
        '''
        This is hopefully the end all to a universal dynamic object attribute constructor
        After over half a dozen iterations I've improved this to hopefully fix all the issues and design flaws I have been encountering the last
        couple of weeks
        Only time will tell - 2022-09-04

        2 days later and I rewrote this because I'm dumb and I could do better lol! - 09-06

        This function takes in a bunch of data passed from any object instance, and uses it to make object attributes dynamically.
        Also does attribute renaming and input validation
        Many lines of code, and my sanity, are saved this way

        self             -- The object in question, what the attributes will be set on
        input_data       -- Data, typically a request response payload, which the attribute values are derived from
        blueprint_plan   -- A dictionary passed from the object which describe which attribute names to set and what their defaults should be
                            (so that every attribute is set regardless if some data in input is missing)
        corrections      -- Attribute names are checked against those from input. However, input's key names can sometimes suck
                            so any items in this dict replace them to match with the objectively better blueprint names

        Additional convention notes:
        - blueprint indexes should be formatted as (attribute_name, default_value, nested default value)
        - correction indexes should be formatted as (expected_name, replacement_name)
        '''
        def compare_values(item, current_value, bp_value, level = 1):
            '''
            Encapsulated comparison logic that validates and configures an input 
            '''
            if isclass(bp_value): # Is a class
                if isinstance(current_value, bp_value):
                    return current_value # No special action
                else: 
                    if type(current_value) == dict: # Checks if dict cuz a new object can be created that way
                        return bp_value(**current_value) # Build object with data
                    elif type(current_value) == type(None):
                        return bp_value()
                    else: # Not instance and not a usable value (dict)
                        raise ObjectInitError(f'Item {item} contains value of type {type(current_value)}, expected {type(bp_value)} or dict')
            else: # Regular data type
                if isinstance(current_value, type(bp_value)):
                    if type(current_value) == list and len(current_value) > 0: # We do a little bit of recursion lololol
                        return [compare_values(item + ' contents', cv_i, bp_value[0], level + 1) for cv_i in current_value] # Handles the contents of an array
                    else:
                        return current_value # No special action
                else: # Didn't match, L
                    if isinstance(current_value, type(None)): # Sometimes values are null, this is a final catch to replace the null with the default without raising an error
                        return bp_value
                    else:
                        raise ObjectInitError(f'Item {item} contains value of type {type(current_value)}, expected {type(bp_value)}')
        

        data = input_data
        blueprint = copy.deepcopy(blueprint_plan)
        # Remember to deep copy

        # Get classes from strings
        # The 'blueprint' variables from formatting.py are designed to contain data class references in order to make creating nested classes much easier.
        # However, this requires formatting.py to import this script, which causes a circular import error. 
        # As a workaround, String names are now where the references were, and these references are put in place here
        globals_ = globals()
        for item in blueprint:
            
            value = blueprint[item]
            is_list = False
            if type(value) == list and len(value) > 0:
                value = value[0]
                is_list = True
            
            if type(value) == str and len(value) > 0:
                if is_list: 
                    blueprint[item] = [globals_[value]]
                else:
                    blueprint[item] = globals_[value]
        
        # Apply corrections
        for fix in corrections: # Note: fix is a key
            if fix in data.keys():
                data[corrections[fix]] = data.pop(fix)
        
        # Some blueprint objects start with a p_, denoting their usage in a post or patch payload. 
        # These prefixes muck up the works big time over here, so they gotta be removed
        for item in blueprint:
            if item[0:1] == 'p_':
                blueprint[item[2:]] = blueprint.pop(item) 
    
        # Constructs a new blueprint using info from data, plus validation
        for item in blueprint:
            if item in data.keys():
                blueprint[item] = compare_values(item, data[item], blueprint[item])
            else: 
                # Blueprint list values typically have something in them (like a class reference) for expected list contents to validate
                # This replaces the filled list with an empty one for usage as a default
                if isinstance(blueprint[item], list):
                    blueprint[item] = []
    
        # Set attributes
        for item in blueprint:
            setattr(self, item, blueprint[item])

        

    def _payload(self): pass

'''
+=+
+=+=+

User Related Classes

+=+=+
+=+
'''


class User(BaseObject):
    '''
    Represents a modrinth user
    '''
    def __init__(self, **args):
        self._build(args, BP_USER, FIX_USER)

        # Replace the string with a datetime
        self.created_at = datetime.fromisoformat(self.created_at[0:23])


class Team(BaseObject):
    '''
    Represents a modrinth team, a collection of users which manage or own a project
    '''
    def __init__(self, **args):
        self._build(args, BP_TEAM)


class TeamMember(BaseObject):
    '''
    Represents a member on a team, a user with extra information regarding the team they're on
    '''
    def __init__(self, **args):
        self._build(args, BP_TEAM_MEMBER, FIX_TEAM_MEMBER)


class Notification(BaseObject):
    '''
    Represents a user's notification on modrinth
    '''
    def __init__(self, **args):
        self._build(args, BP_NOTIFICATION)


'''
+=+
+=+=+

Project Related Classes 

+=+=+
+=+
'''


class Project(BaseObject):
    '''
    Represents a modrinth project
    '''
    def __init__(self, **args):
        self._build(args, BP_PROJECT, FIX_PROJECT)

        # Replace the strings with datetime objects
        self.created_at = datetime.fromisoformat(self.created_at[0:23])
        self.modified_at = datetime.fromisoformat(self.modified_at[0:23])
        try: # Sometimes approved_at is null or after object building an empty string
            self.approved_at = datetime.fromisoformat(self.approved_at[0:23])
        except ValueError:
            self.approved_at = None


class DonationSite(BaseObject):
    '''
    Represents a donation site listing on a project
    '''
    def __init__(self, **args):
        self._build(args, BP_DONATION_SITE)


class ModMessage(BaseObject):
    '''
    Some projects may have this idk what it is yet exactly lmao
    '''
    def __init__(self, **args):
        self._build(args, BP_MOD_MESSAGE)


class Image(BaseObject):
    '''
    Represents a gallery image attached to a project
    '''
    def __init__(self, **args):
        self._build(args, BP_IMAGE, FIX_IMAGE)
    
        # Replace the strings with datetime objects
        self.created_at = datetime.fromisoformat(self.created_at[0:23])


class License(BaseObject):
    def __init__(self, **args):
        self._build(args, BP_LICENSE)


class ProjectListing(BaseObject):
    def __init__(self, **args):
        self._build(args, BP_PROJECT_LISTING)

        # Replace the strings with datetime objects
#       self.created_at = datetime.fromisoformat(self.created_at[0:23])


class SearchResult(BaseObject):
    def __init__(self, **args):
        self._build(args, BP_SEARCH_RESULT)


'''
+=+
+=+=+

Version & File Related Classes 

+=+=+
+=+
'''


class Version(BaseObject):
    '''
    Represents a a version release on a project
    '''
    def __init__(self, **args):
        self._build(args, BP_VERSION, FIX_VERSION)

        # Replace the strings with datetime objects
        self.created_at = datetime.fromisoformat(self.created_at[0:23])


class VersionFile(BaseObject):
    '''
    Represents a file attached to a version
    '''
    def __init__(self, **args):
        self._build(args, BP_VERSION_FILE, FIX_VERSION_FILE)


class Dependency(BaseObject):
    '''
    Some versions have mod dependencies. This represents one
    '''
    def __init__(self, **args):
        self._build(args, BP_DEPENDENCY, FIX_DEPENDENCY)


class DependencyList(BaseObject):
    '''
    Represents a list of *all* dependencies required by a project
    '''
    def __init__(self, **args):
        self._build(args, BP_DEPENDENCY_LIST)
