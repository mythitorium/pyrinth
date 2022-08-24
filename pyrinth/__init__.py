'''
Pyrinth by Mythitorium
'''

import requests
import json

PATH = "https://api.modrinth.com/v2/"
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
    

    def search(self, query):
        result = requests.get(f"{PATH}search?query={query}")
        if result.status_code == 200:
            return SearchResult(json.loads(result.text))
        else:
            return result.status_code


class Project:
    '''
    Represents a modrinth project, either a mod or a modpack
    '''
    def __init__(self, input):
        for key in input.keys(): 
            setattr(self, key, input[key])


class Team:
    pass
    '''
    Represents a modrinth team
    A team is a collection of one or more users who own/manage a project
    '''
    

class User:
    '''
    Represents a modrinth user
    
    '''


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
    Because the structure and composition of the projects returned from a search query are different than a regular get project call, 
    search query project data isn't compatible with the regular Project class. That's the gap this class fills
    '''
    def __init__(self, input):
        # Easy iteration of attributes and their values
        for key in input.keys():
            # Checks for alt attribute name to use instead of the input's
            if key in ALT_ANAMES.keys():
                attribute = ALT_ANAMES[key]
            else:
                attribute = key
            setattr(self, attribute, input[key])