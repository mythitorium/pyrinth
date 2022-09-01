'''

Swagrinth by Mythitorium
++++

TO DO LIST

- Change all timestamps into datetime objects
- Implement filters and tags
- Build a validate class system
- Start buildthedocs site

'''

import requests
from json import *
from datetime import datetime
from .project import *
from .user import *
from .errors import *
from inspect import getmembers, isclass, signature
from .objecthandler import *

PATH = "https://api.modrinth.com/v2/"


class Core:
    '''
    Main class for handling, sending, and requesting data
    '''
    def __init__(self, token="", get_self=False):
        self.token = token

        self.ratelimit = -1
        self.remaining = -1
        self.next_refresh = -1

        self.status = None

        if not get_self:
            self.self = None
        else: 
            self.get_self()
    
    ''' GET REQUESTS '''

    def set_auth(self, token, get_self=False):
        self.token = token
        if get_self: self.get_self()
    
    def get_self(self, return_copy=False):
        result = requests.get(f"{PATH}user", headers={'Authorization': self.token})

        if result.status_code == 200:
            self.self = User(loads(result.text))
            if return_copy: return User(loads(result.text))
        elif result.status_code == 401:
            raise NoAccess("No token")
        else:
            raise NotFound('token', "user by")

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
        validate_var([(query, str),(offset, int),(limit, int)])

        result = requests.get(f"{PATH}search?query={query}&offset={offset}&limit={limit}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return SearchResult(loads(result.text))
        else:
            raise NotFound(query, "search")
    
    def get_project(self, project_id: str):
        '''
        Get a project from its id or slug
        '''
        validate_var([(project_id, str)])

        result = requests.get(f"{PATH}project/{project_id}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Project(loads(result.text))
        else:
            raise NotFound(project_id, "project")

    def get_project_dependencies(self, project_id: str):
        '''
        '''
        validate_var([(project_id, str)])
        
        result = requests.get(f"{PATH}project/{project_id}/dependencies", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            data = loads(result.text)
            return DependencyList(loads(result.text))
        else:
            raise NotFound(project_id, "project")

    def get_project_team(self, project_id: str):
        '''
        Get a team composition from 
        '''
        validate_var([(project_id, str)])

        result = requests.get(f"{PATH}project/{project_id}/members", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(project_id, "project")
    
    def get_team(self, team_id: str):
        validate_var([(team_id, str)])

        result = requests.get(f"{PATH}project/{team_id}/members", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return Team(loads(result.text))
        else:
            raise NotFound(team_id, "team")
    
    def get_user(self, user_id: str):
        validate_var([(user_id, str)])

        result = requests.get(f"{PATH}user/{user_id}", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return User(loads(result.text))
        else:
            raise NotFound(user_id, "user")
    
    def get_user_projects(self, user_id: str):
        validate_var([(project_id, str)])

        result = requests.get(f"{PATH}user/{user_id}/projects", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Project(project) for project in loads(result.text)]
        else:
            raise NotFound(user_id, "user")

    def get_project_versions(self, project_id: str):
        '''
        '''
        validate_var([(project_id, str)])

        result = requests.get(f"{PATH}project/{project_id}/version", headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [ProjectVersion(version_dict) for version_dict in loads(result.text)]
        else:
            raise NotFound(project_id, "project")

    def get_version(self, version_id: str):
        '''
        '''
        validate_var([(version_id, str)])

        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return ProjectVersion(loads(result.text))
        else:
            raise NotFound(version_id, "project version")
    
    def get_followed_projects(self):
        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Projects(project) for project in loads(result.text)]
        elif result.status_code == 401:
            raise NoAccess("No clearance")
        else:
            raise NotFound('token', "user by")
    
    def get_notifs(self):
        result = requests.get(f'{PATH}version/{version_id}', headers={'Authorization': self.token})
        self.update_ratelimit_info(result.headers)

        if result.status_code == 200:
            return [Notification(notif) for notif in loads(result.text)]
        elif result.status_code == 401:
            raise NoAccess("No clearance")
        else:
            raise NotFound('token', "user by")

    ''' MODIFY REQUESTS '''

    def edit_profile(self, username, email = "", displayname = "", bio = ""):
        validate_var([(username, str),(email, str),(displayname, str),(bio, str)])

        payload = {'username' : username}
        if not email == '': payload['email'] = email
        if not displayname == '': payload['name'] = displayname
        if not bio == '': payload['bio'] = bio

        response = requests.patch(f'{PATH}user/{self.self.id}', json = payload, headers={'Authorization': self.token})
        if response.status_code == 404:
            raise NotFound(self.self.id, "user")
        elif response.status_code == 401:
            raise NoAccess("No clearance")
        elif response.status_code == 400:
            print(response.status_code)
            raise BadPayload("Bad data", f'{response.text}')


def init_data_object(source, class_type, input):
    try:
        the_class = getattr(eval(source), class_type)
        print(str(signature(the_class.__init__))[1:-1].split(", ")[1:])
    except AttributeError as reason:
        print(f'{reason}')

