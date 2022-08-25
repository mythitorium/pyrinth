'''
Pyrinth by Mythitorium
'''

import requests
import json
from datetime import datetime
from functions import set_bulk_attr

PATH = "https://api.modrinth.com/v2/"


class Core:
    '''
    Main class for handling, sending, and requesting data

    # TO DO: Add authorization
    '''
    def __init__(self, token=""):
        self.token = token

        self.ratelimit = -1
        self.ratelimit_remaining = -1
        self.ratelimit_refresh = -1
    

    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        result = requests.get(f"{PATH}search?query={query}&offset={offset}&limit={limit}")
        if result.status_code == 200:
            return SearchResult(json.loads(result.text))
        else:
            return result.status_code
    

    def get_project(self, project_id):
        '''
        Get a project from its id or slug
        '''
        result = requests.get(f"{PATH}project/{project_id}")
        if result.status_code == 200:
            return Project(json.loads(result.text))
        else:
            return result.status_code

    
    def get_dependencies(self, project_id):
        pass
    

    def get_project_team(self, project_id):
        '''
        Get a team composition from 
        '''
        result = requests.get(f"{PATH}project/{project_id}/members")
        if result.status_code == 200:
            return Team(json.loads(result.text))
        else:
            return result.status_code
    

    def get_team(self, team_id):
        result = requests.get(f"{PATH}project/{team_id}/members")
        if result.status_code == 200:
            return Team(json.loads(result.text))
        else:
            return result.status_code
    

    def get_user(self, user_id):
        result = requests.get(f"{PATH}user/{user_id}")
        if result.status_code == 200:
            return User(json.loads(result.text))
        else:
            return result.status_code


class Project:
    '''
    Represents a modrinth project, either a mod or a modpack
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['gallery','published','modified'])
        self.created_at = input['published']
        self.updated_at = input['modified']
        self.gallery = [Image(image) for image in input['gallery']]


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


class SearchResult:
    '''
    Represents a search result.
    Searching modrinth's mod list will return a list of mods given the request query parameters
    '''
    def __init__(self, input):
        self.results = [ProjectListing(hit) for hit in input['hits']]
        self.total_hits = input["total_hits"]


class ProjectListing:
    '''
    A variation of the Project class
    This class exists because the structure and composition of project data returned from a search query 
    is vastly different than that of a regular get project call
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['date_created','date_modified'])
        self.created_at = input['date_created']
        self.updated_at = input['date_modified']


class Image:
    '''
    Represents a gallery image
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)
