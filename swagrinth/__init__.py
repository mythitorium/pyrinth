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
from .formatting import *

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
        ''' Returns rate limit info as a dict '''
        return {'ratelimit' : self.ratelimit, 'remaining' : self.remaining, 'next_refresh' : self.next_refresh}


    def search(self, query, offset=0, limit=10):
        '''
        Requests a search on modrinth's database

        # DO TO: Implement facets and filters
        '''
        valid_type_table = {'query' : (query, str), 'offset' : (offset, int), 'limit' : (limit, int)}
        validate_objects(valid_type_table)

        result = requests.get(f'{PATH}search?query={query}&offset={offset}&limit={limit}', headers={'Authorization': self.token})
        self._update_ratelimit_info(result.headers)
        self._check_response(result, f"Search by query '{query}'")

        return SearchResult(**loads(result.text))


    def get(self, get_type: str, target_id = ''):
        '''
        multi-purpose get function for requesting data from modrinth

        get_type : phrase to signify what endpoint data should be retrieved from
        target_id : What data should be requested (a user, a project, etc)  
        '''
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


    def get_multiple(self, get_type: str, target_ids = []):
        '''
        multi-purpose get function for requesting multiple sets of data from modrinth
        modrinth has some built-in endpoints for getting arrays of data objects, this function utilizes them

        get_type : phrase to signify what endpoint data should be retrieved from
        target_id : What data should be requested (a user, a project, etc)
        '''
        # Lookup table
        req_lookup = {
            'users' :    (f'users?ids={target_ids}',     User,    'Erm.... what the flock...'),
            'projects' : (f'projects?ids={target_ids}',  Project, 'Erm.... what the flock...'),
            'versions' : (f'versions?ids={target_ids}',  Version, 'Erm.... what the flock...'),
            'teams' :    (f'teams?ids={target_ids}',     Team,    'Erm.... what the flock...'),
        }

        # Error handling
        if not get_type in req_lookup.keys():
            raise TypeError(f"Get_type value '{get_type}' isn't valid")
        valid_type_table = {'get_type' : (get_type, str), 'target_ids' : (target_ids, list)}
        validate_objects(valid_type_table)
        # Check the contents of target_ids
        valid_content_table = {}
        for ind in range(0, len(target_ids)):
            valid_content_table[f'target_ids index {ind}'] = (target_ids[ind], str)
        validate_objects(valid_content_table)

        # Object handling
        req_info = req_lookup[get_type]
        # Replace ' with "
        # Because query interpreter hates it when it gets strings denoted with '
        new_endpoint = ''
        for char in req_info[0]:
            if char == "'":
                new_endpoint += '"'
            else:
                new_endpoint += char
        # Request
        result = requests.get(f'{PATH}{new_endpoint}', headers={'Authorization': self.token})
        self._update_ratelimit_info(result.headers)
        self._check_response(result, req_info[2])

        # Object building
        data = loads(result.text)
        if req_info[1] == Team: # Team needs to be built differently
            return [req_info[1](**{'members' : subdata}) for subdata in data]
        else:
            return [req_info[1](**subdata) for subdata in data]



