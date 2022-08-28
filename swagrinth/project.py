'''
Project class and sub classes
'''

from .functions import *
from .base import *


class Project(BaseClass):
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


class ProjectVersion:
    '''
    Represents a project 'version'
    Contains information about a specific mod release, dependencies, and any given download files
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['files','dependencies'])
        self.files = [ProjectFile(i) for i in input['files']]
        self.dependencies = [Dependency(e) for i in input['dependencies']]


class ProjectFile:
    '''
    Represents a downloadable file within a project version
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['hashes'])
        self.hash_sha512 = input['hashes']['sha512']
        self.hash_sha1 = input['hashes']['sha1']


class Dependency:
    '''
    Represents a 'dependency' for a project version, information pointing to another project
    '''
    def __init__(self, input):
        set_bulk_attr(self, input, ['version_id','project_id'])
        if 'version_id' in input:
            self.type = 'version'
            self.id = input['version_id']
        else:
            self.type = 'project'
            self.id = input['project_id']


class DependencyList:
    '''
    Represents a collection of all dependencies a project has
    '''
    def __init__(self, input):
        self.projects = [Project(project) for project in input['projects']]
        self.versions = [ProjectVersion(version) for version in input['versions']]


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
