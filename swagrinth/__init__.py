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
    def __init__(self, token=""):
        self.token = token

        self.ratelimit = -1
        self.remaining = -1
        self.next_refresh = -1


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


    def set_auth(self, token):
        self.token = token
    

    def get_ratelimit(self):
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        valid_type_table = {'query' : (query, str), 'offset' : (offset, int), 'limit' : (limit, int)}
        validate_objects(valid_type_table)

        results = requests.get(f'{PATH}search?query={query}&offset={offset}&limit={limit}', headers={'Authorization': self.token})
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Search by query '{query}'")

        return SearchResult(**loads(result.text))


    def get(self, get_type: str, target_id = ''):
        # Lookup table
        # type : endpoint, return type, debug info
        req_lookup = {
            'project' :      (f'project/{target_id}',               Project,         f"Project by id/slug '{target_id}'"),
            'user' :         (f'user/{target_id}',                  User,            f"User by id/slug '{target_id}'"),
            'team' :         (f'user/{target_id}',                  Team,            f"Team by id '{target_id}'"),
            'team_project' : (f'project/{target_id}/members',       Team,            f"Team by project id/slug '{target_id}'"),
            'version' :      (f'version/{target_id}',               Version,         f"Version by id '{target_id}'"),
            'dependencies' : (f'project/{target_id}/dependencies',  DependencyList,  f"Project by id/slug '{target_id}'"),
            'self' :         (f'user',                              User,            f"User by token"),
        }

        # Error handling
        if not get_type in req_lookup.keys():
            raise TypeError(f"Get_type value '{get_type}' isn't valid")
        valid_type_table = {'get_type' : (get_type, str), 'target_id' : (target_id, str)}   
        validate_objects(valid_type_table)
        
        # Request handling
        req_info = req_lookup[get_type]
        result = requests.get(f'{PATH}{req_info[0]}', headers={'Authorization': self.token})
        self._update_ratelimit_info(result.headers)
        self._check_response(result, req_info[2])

        # Object building
        data = loads(result.text)
        if req_info[1] == Team: # Team needs to be built differently
            return Team(**{'members' : data})
        else:
            return req_info[1](**data)


