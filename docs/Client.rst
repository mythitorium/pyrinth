.. currentmodule:: swagrinth

Client
========


.. class:: Client(token = '')

  


    Used to interact with modrinth's API.

    Everything in centralized around this class. This class is used as a sole interaction with modrinth's API, 
    and all other classes act as data containers to house data this class retrieves

    Providing a token is optional, however you won't be able to access data (which you would be able to while logged in) without one.

    If you don't provide token while instancing, you always can at any point using ``set_token()``


    .. method:: get(get_type, target_id = '')

        Multi-purpose for retrieving data from Modrinth. ``get_type`` is used to determine what endpoint to get from, and ``target_id`` is the id or name of the object.

        Both ``get_type`` and ``target_id`` must be strings.

        ``get_type`` can be a multitude of different values, each returning a different object type:

        - ``'user'`` : For getting a user. Expects ``target_id`` to be a user's id or name. Returns User
        - ``'project'`` : For getting a project. Expects ``target_id`` to be a project's id or slug. Returns Project
        - ``'team'`` : For getting a team. Expects ``target_id`` to be the id of a team. Returns Team
        - ``'team_project'`` : For getting a team. Expects ``target_id`` to be the id of a project. Returns Team
        - ``'version'`` : For getting a project version. Expects ``target_id`` to be the id of a project version. Returns Version
        - ``'dependencies'`` : For getting a collection of all projects and versions a specific project has listed as dependencies. Expects ``target_id`` to be the id of a project. Returns DependencyList
        - ``'self'`` : For getting the user by the token, but won't work if the value of ``token`` isn't a valid token. ``target_id`` Is ignored. Returns User

  
    .. method:: get_multiple(get_type, target_ids)

        Multi-purpose for retrieving data from Modrinth.  ``get_type`` is used to determine what endpoint to get from, and ``target_ids`` is the list of objects to get
  
        ``get_type`` must be a string, ``target_ids`` must be a list of strings
  
        Differs from ``get()`` by allowing to get multiple objects from Modrinth at once.
  
        ``get_type`` can be a multitude of different values, each returning a list with a different object type:
  
        - ``'users'`` : For getting multiple users. Expects ``target_ids`` to contain user ids. Returns a list of Users
        - ``projects`` : For getting multiple projects. Expects ``target_ids`` to contain project ids. Returns a list of Projects
        - ``teams`` : For getting mutliple teams. Expects ``target_ids`` to contain team ids. Returns a list of Teams
        - ``versions`` : For getting multiple versions. Expects ``target_ids`` to contain project version ids. Returns a list of Versions
  

    .. method:: search(query, offset = 0, limit = 10)

        Preforms a search of Modrinth's mod catalogue. ``query`` is the search term to search by, ``limit`` is the maximum amount of hits to return, and ``offset`` notes the offset the ``limit`` results should be taken from

        ``query`` must be a string, ``limit`` and ``offset`` must be integers

        Returns a SearchResult


    .. method:: set_auth(token)

        Sets the class's ``token`` attribute to the given ``token`` input.

        ``token`` must be a string.


    .. property:: token

        Stores a Modrinth user token, which is used to validate requests. While having one is optional, some data is inaccessible without giving one

        Defaults to ``''``
