'''
Project class and sub classes
'''

from .functions import *


class Project:
    '''
    Represents a modrinth project, either a mod or a modpack
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['gallery','published','modified'])
        self.created_at = input['published']
        self.updated_at = input['updated']
        self.gallery = [Image(image) for image in input['gallery']]


class SearchResult:
    '''
    Represents a search result.
    Searching modrinth's mod list will return a list of mods given the request query parameters
    '''
    def __init__(self, input):
        self.results = [ProjectListing(hit) for hit in input['hits']]
        self.total_hits = input["total_hits"]


class ProjectListing:
    '''
    A variation of the Project class
    This class exists because the structure and composition of project data returned from a search query 
    is vastly different than that of a regular get project call
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['date_created','date_modified'])
        self.created_at = input['date_created']
        self.updated_at = input['date_modified']


class Image:
    '''
    Represents a gallery image
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)


class License:
    '''
    Represents a project's copyright license
    ''' 
    def __init__(self, input):
        set_bulk_attr(self, input)


class DonationSite:
    '''
    Represents a donation site a project may have
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)


class ModMessage:
    '''
    Represents a mod message on a project
    '''
    def __init__(self, input):
        set_bulk_attr(self, input)
