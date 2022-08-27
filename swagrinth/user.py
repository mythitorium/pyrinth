'''
Classes related to users and teams
'''

from .functions import *
from .base import *


class Team(BaseClass):
    '''
    Represents a modrinth team.
    A team is a collection of one or more users who own/manage a project
    '''
    def __init__(self, input):
        self.members = [TeamMember(member) for member in input]
        self.id = input[0]['team_id']


class TeamMember(BaseClass):
    '''
    Represents a member of a team.
    Team members are made up of a user and metadata about their role in the team
    '''
    def __init__(self, input):
        self.team_id = input['team_id']
        self.user = User(input['user'])
        self.role = input['role']
        self.perms = input['permissions'] # TO DO: Use a dictionary or class instead of a bitflag
        self.accepted = input['accepted']
    

class User(BaseClass):
    '''
    Represents a modrinth user
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)


class MemberPerms(BaseClass):
    '''
    Represents a team member's permissions
    Turns a bitflag into a bunch of booleans
    '''
    def __init__(self, input):
        attributes = ['upload_version','delete_version','edit_details','edit_body','manage_invites','remove_member','edit_member','delete_project']
        if input == None:
            for attr in attributes:
                setattr(self, attr, None)
        else:
            for index in 8:
                setattr(self, attributes[index], bool(input[index]))

