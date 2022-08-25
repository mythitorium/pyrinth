'''
Pyrinth by Mythitorium
'''

import requests
import json
from datetime import datetime

PATH = "https://api.modrinth.com/v2/"
'''
I made this because the date of creation and latest modification for projects returned via a get project call and via search call are named differently for some reason.
Because of how I dynamically assign attributes to my container classes, this (and other inconsistencies I have yet to find)
will end up as attributes for my classes, which I don't want

This just defines key name replacements 
'''
ALT_ANAMES = {
    "date_created" : "created_at", 
    "date_updated" : "updated_at",
    "published" : "created_at",
    "modified" : "updated_at",

    "created" : "created_at"
}


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

    
    def get_dependencies(self, project_id)
    

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
        attribute_init(self, input, "Project", ["Gallery"])
        self.gallery = [Image(image) for image in input.gallery]


class Team:
    '''
    Represents a modrinth team.
    A team is a collection of one or more users who own/manage a project
    '''
    def __init__(self, input):
        self.members = []
        for member in input['members']:
            self.members.append(TeamMember(member))
        self.id = input['members'][0]['team_id']


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
        attribute_init(self, input, "User")


class SearchResult:
    '''
    Represents a search result.
    Searching modrinth's mod list will return a list of mods given the request query parameters
    '''
    def __init__(self, input):
        projects = []
        # Turn each hit into a ProjectListing 
        for hit in input["hits"]:
            projects.append(ProjectListing(hit))
        self.results = projects
        self.total_hits = input["total_hits"]


class ProjectListing:
    '''
    A variation of the Project class
    This class exists because the structure and composition of project data returned from a search query 
    is vastly different than that of a regular get project call
    '''
    def __init__(self, input):
        attribute_init(self, input, "ProjectListing")


class Image:
    '''
    Represents a gallery image
    '''
    def __init__(self, input):
        attribute_init(self, input, "Image")


def attribute_init(target_class, input_dict, class_type, exceptions):
    '''
    Function that handles assigning mass attributes to container classes
    In a function instead of the class init's themselves so I don't have to manage the same lines of code across a million places

    TO DO: Error checking
    '''
    for key in input_dict.keys():
        if not key in exceptions:
            # Checks for alt attribute name to use instead of the input's
            if key in ALT_ANAMES.keys():
                attribute = ALT_ANAMES[key]
            else:
                attribute = key
            setattr(target_class, attribute, input_dict[key])
