'''
Classes related to users and teams
'''


class Team:
    '''
    Represents a modrinth team.
    A team is a collection of one or more users who own/manage a project
    '''
    def __init__(self, input):
        self.members = [TeamMember(member) for member in input]
        self.id = input[0]['team_id']


class TeamMember:
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
    

class User:
    '''
    Represents a modrinth user
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)