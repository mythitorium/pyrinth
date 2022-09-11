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
    

    def _handle_request(endpoint: str, info: str):
        '''
        Does the thing with the requests and the other thing
        So I don't have write this crap a million times
        '''
        # Get data
        result = requests.get(f'{PATH}{endpoint}', headers=self._auth_header)
        # Update rate limit vars
        self._update_ratelimit_info(result.headers)
        # Check response
        self._check_response(result, info)

        return loads(result.text)


    def _update_ratelimit_info(self, headers):
        self.ratelimit = headers['X-Ratelimit-Limit']
        self.remaining = headers['X-Ratelimit-Remaining']
        self.next_refresh = headers['X-Ratelimit-Reset']


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


    def set_auth(self, token, get_self=False):
        self.token = token
        self._auth_header = {'Authorization': self.token}
        if get_self: self.get_self()
    

    def get_self(self, return_copy=False):
        data = _handle_request('user', 'User by token')
        self.self = User(data)
        if return_copy: return User(data)


    def get_ratelimit(self):
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        validate_object([query], str)
        validate_object([offset, limit], int)

        data = _handle_request(f'{PATH}search?query={query}&offset={offset}&limit={limit}', f"Search by query '{query}'")
        return SearchResult(data)


    def get_user(self, user_id: str):
        validate_object([user_id], str)

        data = _handle_request(f'{PATH}user/{user_id}', f"User by id/slug '{user_id}'")
        return User(data)


    def get_project(self, project_id: str):
        validate_object([project_id], str)

        data = _handle_request(f'project/{project_id}', f"Project by id/slug '{project_id}'")
        return Project(**data)


    def get_team(self, team_id: str):
        validate_object([team_id], str)

        data = _handle_request(f'team/{team_id}', f"Team by id/slug '{team_id}'")
        return Team(**{'members' : data})


    def get_project_team(self, project_id: str):
        validate_object([project_id], str)

        data = _handle_request(f'project/{project_id}/members', f"Team by project id/slug '{project_id}'")
        return Team(**{'members' : data})


