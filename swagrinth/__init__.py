'''

Swagrinth by Mythitorium


'''

import requests
from json import *
from datetime import datetime
from .classes2 import *
from .errors import *
from inspect import getmembers, isclass, signature
from .handler import *

PATH = 'https://api.modrinth.com/v2/'


class Client:
    '''
    Main class for handling, sending, and requesting data
    '''
    def __init__(self, token="", get_self=False):
        self.token = token
        self._auth_header = {'Authorization': self.token}

        self.ratelimit = -1
        self.remaining = -1
        self.next_refresh = -1

        self.status = None

        if not get_self:
            self.self = None
        else: 
            self.get_self()
    

    def set_auth(self, token, get_self=False):
        self.token = token
        self._auth_header = {'Authorization': self.token}
        if get_self: self.get_self()
    

    def get_self(self, return_copy=False):
        result = requests.get(f'{PATH}user', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, 'User by token')

        self.self = User(loads(result.text))
        if return_copy: return User(loads(result.text))


    def _update_ratelimit_info(self, headers):
        self.ratelimit = headers['X-Ratelimit-Limit']
        self.remaining = headers['X-Ratelimit-Remaining']
        self.next_refresh = headers['X-Ratelimit-Reset']


    def get_ratelimit(self):
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def _check_response(self, response, info):
        '''
        Encapsulated logic for checking response errors
        '''
        if response.status_code == 400: # Sent bad payload
            raise BadPayload(f'Bad data, {response.text}')
        elif response.status_code == 401: # No access
            raise NoAccess(f'No valid authorization')
        elif response.status_code == 404: # Not found
            raise NotFound(f'Data about {info} not found')


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        validate_object([query], str)
        validate_object([offset, limit], int)

        result = requests.get(f'{PATH}search?query={query}&offset={offset}&limit={limit}', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Search by query '{query}'")

        return SearchResult(loads(result.text))


    def get_user(self, user_id: str):
        validate_object([user_id], str)

        result = requests.get(f'{PATH}user/{user_id}', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"User by id/slug '{user_id}'")

        return User(loads(result.text))


    def get_project(self, project_id: str):
        validate_object([project_id], str)

        result = requests.get(f'{PATH}project/{project_id}', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Project by id/slug '{project_id}'")

        return Project(**loads(result.text))


    def get_team(self, team_id: str):
        validate_object([team_id], str)

        result = requests.get(f'{PATH}team/{team_id}', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Team by id/slug '{team_id}'")

        return Team(**{'members' : loads(result.text)})


    def get_project_team(self, project_id: str):
        validate_object([project_id], str)

        result = requests.get(f'{PATH}project/{project_id}/members', headers=self._auth_header)
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Team by project id/slug '{project_id}'")

        return Team(**{'members' : loads(result.text)})



