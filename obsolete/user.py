'''
Classes related to users and teams
'''

from inspect import *
from .handler import *

class Team():
    '''
    Represents a modrinth team.
    A team is a collection of one or more users who own/manage a project
    '''
    def __init__(self, input):
        self.members = [TeamMember(member) for member in input]
        self.id = input[0]['team_id']


class TeamMember():
    '''
    Represents a member of a team.
    Team members are made up of a user and metadata about their role in the team
    '''
    def __init__(self, input):
        self.team_id = input['team_id']
        self.user = User(input['user'])
        self.role = input['role']
        self.perms = MemberPerms(input['permissions'])
        self.accepted = input['accepted']
    

class User():
    '''
    Represents a modrinth user
    '''
    def __init__(self, input):
        bulk_attr_set(self, locals())


class MemberPerms():
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


class Notification():
    '''
    Represents a user notification
    '''
    def __init__(self, input):
        self.set_bulk_attr(self, input)

