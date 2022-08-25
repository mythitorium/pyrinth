'''
Pyrinth by Mythitorium
'''

import requests
import json
from datetime import datetime
from .project import *
from .user import *

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
