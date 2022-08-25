'''
Pyrinth by Mythitorium
'''

import requests
import json

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
    "modified" : "updated_at"
}


class Core:
    '''
    Main class for handling, sending, and requesting data

    # TO DO: Add authorization
    '''
    def __init__(self, token=""):
        self.token = token
    

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
        result = requests.get(f"{PATH}project/{project_id}")
        if result.status_code == 200:
            return Project(json.loads(result.text))
        else:
            return result.status_code
    

    def get_project_team(self, project_id):
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


class Project:
    '''
    Represents a modrinth project, either a mod or a modpack
    '''
    def __init__(self, input):
        attribute_init(self, input, "Project")


class Team:
    '''
    Represents a modrinth team
    A team is a collection of one or more users who own/manage a project
    '''
    def __init__(self, input):
        attribute_init(self, input, "Team")
    

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


class ProjectListing():
    '''
    A variation of the Project class
    This class exists because the structure and composition of project data returned from a search query 
    is vastly different than that of a regular get project call
    '''
    def __init__(self, input):
        attribute_init(self, input, "ProjectListing")


def attribute_init(target_class, input_dict, class_type):
    '''
    Function that handles assigning mass attributes to container classes
    In a function instead of the class init's themselves so I don't have to manage the same lines of code across a million places

    TO DO: Error checking
    '''
    for key in input_dict.keys():
        # Checks for alt attribute name to use instead of the input's
        if key in ALT_ANAMES.keys():
            attribute = ALT_ANAMES[key]
        else:
            attribute = key
        setattr(target_class, attribute, input_dict[key])
