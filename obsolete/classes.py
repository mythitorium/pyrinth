'''
Data classes
'''

from datetime import datetime
from .handler import *
from inspect import isclass
from .formatting import *
from .errors import *


'''
User related classes
'''


class User:
    '''
    Represents a modrinth user

    Modrinth User Model
    +=+=+
    username   : Username
    name       : Display name
    email      : User's email 
    bio        : About me bio
    id         : Unique id
    github_id  : User's github id
    avatar_url : Url to the user's avatar
    created    : ISO-8601 of the creation of the user's account
    role       : What role this user has (dev, mod, or admin)
    '''

    def __init__(self, *args):
        build()


    def build(self, payload):
        # Bulk set
        attr_set(self, payload, ['user_id', 'username', 'email', 'bio', 'github_id', 'avatar_url', 'role'])
        self.display_name = payload['name']
        # Use a datetime object
        self.created_at = datetime.fromisoformat(payload['created'])

    def get_as_payload():
        '''
        Returns attributes (as a dictionary) relevant to being sent as a payload
        '''
        return {'username' : str(self.username), 'name' : str(self.display_name), 'email' : str(self.email), 'bio' : str(self.bio)}


class Team:
    '''
    Represents a Modrinth Team, a collection of users who have special permissions regarding a project

    Modrinth Team Model
    +=+=+
    []     : An array of team members
    '''

    def __init__(self):
        self.team_members = []
    
    def build(self, payload):
        for bit in payload:
            member = TeamMember()
            member.build(bit)
            team_members.append(member)


class TeamMember:
    '''
    Represents a member of a team.
    Team members are made up of a user and metadata about their role in the team

    Modrinth Team Member Model
    +=+=+
    id          : The id of the team this team member belongs to
    user        : The user this team member represents
    role        : Member's role
    permissions : Permissions bitflag
    accepted    : If the user has been accepted into the team (only visible with valid auth)
    '''

    def __init__(self):
        pass


    def build(self, payload):
        # Attr set
        attr_set(self, payload, ['accepted', 'role'])
        self.team_id = payload['id']
        self.user = User()
        self.user.build(payload['user'])
        self.permissions = MemberPerms()
        self.permissions.build(payload['permissions'])


class Notification:
    '''
    Represents a user's notification

    Modrinth Notification Model
    +=+=+
    id       : Notif id
    user_id  : Id of the user who got the notif
    type     : Type
    title    : Title
    text     : Body
    link     : Link to related project or version
    read     : Whether or not the user has read this notif
    created  : ISO-8601 of when the notif was made
    actions  : Relevant actions, if any
    '''

    def __init__(self, notif_id='', user_id='', notif_type='', title='', body='', link='', read=False, created_at=''):
        # Validation
        validate_object([user_id, notif_type, title, body, link, ], str)
        is_valid_time(created_at)

        # Attr set
        attr_set(self, locals(), [notif_id, user_id, notif_type, title, body, link, read])
        self.created_at = datetime.fromisoformat(created_at)


class MemberPerms:
    '''
    Represents a set of permissions a team member may have

    Modrinth permissions model: bitfield lol 
    '''

    def __init__(
            self, upload_version=False, delete_version=False, edit_details=False, edit_body=False, 
            manage_invites=False, remove_member=False, edit_member=False, delete_project=False 
            ):
        validate_object([upload_version, delete_version, edit_details, edit_body, manage_invites, remove_member, edit_member, delete_project], bool)
        attr_set(self, locals(), [upload_version, delete_version, edit_details, edit_body, manage_invites, remove_member, edit_member, delete_project])

    def get_as_bitfield(self):
        '''
        Convert boolean attributes into a bitflag
        '''
        attrs = [self.upload_version, self.delete_version, self.edit_details, self.edit_body, self.manage_invites, self.remove_member, self.edit_member, self.delete_project]
        field = ''
        for attr in attrs:
            field += f'{int(attr)}'
        return int(field)


'''
Project related classes
'''

class Project:
    '''
    Represents a project

    Modrinth Project Model
    +=+=+
    id                     : Id of the project
    slug                   : Vanity url name of the project
    title                  : Name of the project
    description            : Project description
    body                   : Main body
    categories             : 
    client_side            : Status of client side support
    server_side            : Status of server side support
    additional_categories  : 
    issues_url             : Url to issues site
    source_url             : Url to source code
    wiki_url               : Url to wiki
    discord_url            : Url to discord
    donation_urls          : Collection of linked donation sites
    project_type           : Project type, mod, modpack or resource pack
    downloads              : Number of total downloads
    icon_url               : Url to the project icon
    team_id                : Id of the team for this project
    moderator_message      : 
    published              : ISO-8601 of project creation
    updated                : ISO-8601 of project's latest update or modification
    approved               : ISO-8601 of project's approval date
    followers              : Total project followers
    status                 : Status of the project, approved, unlisted, etc
    license                : Collection of project licenses
    versions               : Collection of project versions
    gallery                : Collection of preview images
    '''

    def __init__(self, *args):
        build_obj(self, args, BP_PROJECT, FIX_PROJECT)
        

'''
Some Other Functions Lol
'''

def build(object_, input: dict, blueprint: list, corrections: list):
    '''
    This is hopefully the end all to a universal dynamic object attribute constructor
    After over half a dozen iterations I've improved this to hopefully fix all the issues and design flaws I have been encountering the last
    couple of weeks
    Only time will tell - 2022-09-04

    This function takes in a bunch of data passed from any object instance, and uses it to make object attributes dynamically.
    Also does attribute renaming and input validation
    Many lines of code, and my sanity, are saved this way

    object_     -- The object in question, what the attributes will be set on
    input       -- Data, typically a request response payload, which the attribute values are derived from
    blueprint   -- A array or tuples passed from the object which describe which attribute names to set and what their defaults should be
                   (so that every attribute is set regardless if some data in input is missing)
    corrections -- Attribute names are checked against those from input. However, input's key names can sometimes suck
                   so any tuples in this array replace them to match with the objectively better blueprint names

    Additional convention notes:
    - blueprint indexes should be formatted as (attribute_name, default_value, nested default value)
    - correction indexes should be formatted as (expected_name, replacement_name)
    '''
    # I only want attributes to be of correct type. Raising an error before building an object forces this
    for item in blueprint: # note: item is a tuple 
        if item[0] in input.keys():
            # Compare the value of input to the key name of item
            # Basic datatypes
            if type(item[1]) in [str, int, list]:
                if not isinstance(input[item[0]], type(item[1])): 
                    raise ObjectInitError(f'Attribute {item[0]} expected a value of type {type(item[1])}, got {type(input[item[0]])}')
            # Classes
            else:
                if not isinstance(input[item[0]], item[1]):
                    raise ObjectInitError(f'Attribute {item[0]} expected a value of object {item[1]}, got {input[item[0]]}')

    fixed_blueprint = blueprint
    # Applies corrections
    for fix in corrections: # note: fix is a tuple 
        if fix[0] in fixed_blueprint.keys():
            fixed_blueprint[fix[1]] = fixed_blueprint.pop(fix[0])
    
    # Validate contents and set attributes
    for item in fixed_blueprint: # note: item is a tuple
        # Validate


        # Set
        
        # Named variables for readability
        bp_name = item[0]
        bp_d_value = item[1]
        bp_nested_value = None
        try: bp_nested_value = item[2]
        except: pass
        
        if bp_name in input.keys():     
            if isinstance(input[bp_name], list): # If it's a list, handle it's indexes
                if len(input[bp_name]) == 0: # List is empty, just use that
                    setattr(object_, bp_name, input[bp_name])
                elif isinstance(input[bp_name][0], dict) and isclass(bp_nested_value):  # List has dicts, and blueprint lists a class
                    setattr(object_, bp_name, [bp_nested_value(nested_dict) for nested_dict in input[bp_name]])
                else: setattr(object_, bp_name, input[bp_name]) # List has anything else
           
            elif isinstance(input[bp_name], dict) and isclass(bp_d_value):  # If it's a dict, attempt to handle it as a class 
                setattr(object_, bp_name, bp_d_value(input[bp_name]))
    
            else: # No extra handling
                setattr(object_, bp_name, input[bp_name])
        else:
            setattr(object_, bp_name, bp_d_value) # Set to default



def build_obj(object_, input_data: dict, blueprint_plan: dict, corrections: dict):
    '''
    This is hopefully the end all to a universal dynamic object attribute constructor
    After over half a dozen iterations I've improved this to hopefully fix all the issues and design flaws I have been encountering the last
    couple of weeks
    Only time will tell - 2022-09-04

    2 days later and I rewrote this because I'm dumb and I could do better lol! - 09-06

    This function takes in a bunch of data passed from any object instance, and uses it to make object attributes dynamically.
    Also does attribute renaming and input validation
    Many lines of code, and my sanity, are saved this way

    object_          -- The object in question, what the attributes will be set on
    input_data       -- Data, typically a request response payload, which the attribute values are derived from
    blueprint_plan   -- A dictionary passed from the object which describe which attribute names to set and what their defaults should be
                        (so that every attribute is set regardless if some data in input is missing)
    corrections      -- Attribute names are checked against those from input. However, input's key names can sometimes suck
                        so any items in this dict replace them to match with the objectively better blueprint names

    Additional convention notes:
    - blueprint indexes should be formatted as (attribute_name, default_value, nested default value)
    - correction indexes should be formatted as (expected_name, replacement_name)
    '''
    def compare_values(item, current_value, bp_value):
        '''
        Encapsulated comparison logic that validates and configures an input 
        '''
        if isclass(bp_value): # Is a class
            if isinstance(current_value, bp_value):
                return current_value # No special action
            else: 
                if type(current_value) == dict: # Checks if dict cuz a new object can be created that way
                    return bp_value(current_value) # Build object with data
                else: # Not instance and not a usable value (dict)
                    raise ObjectInitError(f'Item {item} contains value of type {type(current_value)}, expected {type(bp_value)} or dict')
        else: # Regular data type
            if isinstance(current_value, type(bp_value)):
                if type(current_value) == list and len(current_value) > 0: # We do a little bit of recursion lololol
                    return [compare_values(item + ' contents', cv_i, bp_value[0]) for cv_i in current_value] # Handles the contents of an array
                else:
                    return current_value # No special action
            else: # Didn't match, L
                raise ObjectInitError(f'Item {item} contains value of type {type(current_value)}, expected {type(bp_value)}')

    # NOTE: To do: Add funny p_ filtering

    data = input_data[0]
    blueprint = blueprint_plan

    # Apply corrections
    for fix in corrections: # Note: fix is a key
        if fix in data.keys():
            data[corrections[fix]] = data.pop(fix)
    
    # Constructs a new blueprint using info from data, plus validation
    for item in blueprint:
        if item in data.keys():
            blueprint[item] = compare_values(item, data[item], blueprint[item])
        else: 
            # Blueprint list values typically have something in them (like a class reference) for expected list contents to validate
            # This replaces the filled list with an empty one
            if isinstance(blueprint[item], list):
                blueprint[item] = []
    
    # Set attributes
    for item in blueprint:
        setattr(object_, item, blueprint[item])




def attr_set(object_, args: dict, attrs = [], make_empty = False):
    '''
    Sets function arguments to object
    '''
    for a in attrs:
        if not make_empty:
            setattr(object_, a, args[a])
        else:
            setattr(object_, a, '')


def attr_to_dict(object_, keys = []):
    '''
    Turns given attributes of an object into a dictionary
    '''
    attrs = get_members(object_)
    payload = {}
    for attr in attrs:
        if attr[0].lower() in keys:
            payload[attr[0]] = attr[1]
    return payload
