'''
Swagrinth by Mythitorium
'''

import requests
from json import loads
from datetime import datetime
from .project import *
from .user import *
from .errors import *

PATH = "https://api.modrinth.com/v2/"


class Core:
    '''
    Main class for handling, sending, and requesting data

    # TO DO: Add authorization
    '''
    def __init__(self, token=""):
        self.token = token

        self.ratelimit = -1
        self.remaining = -1
        self.next_refresh = -1

        self.status = None
    

    def update_ratelimit_info(self, headers):
        self.ratelimit = headers['X-Ratelimit-Limit']
        self.remaining = headers['X-Ratelimit-Remaining']
        self.next_refresh = headers['X-Ratelimit-Reset']
    

    def get_ratelimit(self):
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        validate_args([query, offset, limit],[str, int, int])

        result = requests.get(f"{PATH}search?query={query}&offset={offset}&limit={limit}")
        if result.status_code == 200:
            return SearchResult(loads(result.text))
        else:
            raise NotFound(query, "search")
    

    def get_project(self, project_id: str):
        '''
        Get a project from its id or slug
        '''
        validate_args([project_id],[str])
        result = requests.get(f"{PATH}project/{project_id}")
        self.update_ratelimit_info(result.headers)
        if result.status_code == 200:
            return Project(loads(result.text))
        else:
            raise NotFound(project_id, "project")

    
    def get_dependencies(self, project_id):
        pass
    

    def get_project_team(self, project_id):
        '''
        Get a team composition from 
        '''
        validate_args([project_id],[str])

        result = requests.get(f"{PATH}project/{project_id}/members")
        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(project_id, "project")
    

    def get_team(self, team_id):
        validate_args([team_id],[str])

        result = requests.get(f"{PATH}project/{team_id}/members")
        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(team_id, "team")
    

    def get_user(self, user_id):
        validate_args([user_id],[str])

        result = requests.get(f"{PATH}user/{user_id}")
        if result.status_code == 200:
            return User(loads(result.text))
        else:
            raise NotFound(user_id, "user")
    

    def get_project_versions(self, project_id):
        '''
        '''
        validate_args([project_id],[str])

        result = requests.get(f"{PATH}project/{project_id}/version")
        if result.status_code == 200:
            return [ProjectVersion(version_dict) for version_dict in loads(result.text)]
        else:
            raise NotFound(project_id, "project")
    

    def get_version(self, version_id):
        '''
        '''
        validate_args([version_id],[str])

        result = requests.get(f'{PATH}version/{version_id}')
        if result.status_code == 200:
            return ProjectVersion(loads(result.text))
        else:
            raise NotFound(version_id, "project version")
