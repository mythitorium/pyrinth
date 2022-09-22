Swagrinth Documentation
==============

--------------

Swagrinth is a API wrapper for Modrinth, written in Python

What you can do:
 - Retrieve data from modrinth's database. Projects, Users, Files, you name it
\

What you can't do (YET!):
 - Send data (ie modifying or creating projects)
 - troll face (soon)

I wanted to make a simple wrapper that was easy to understand and use.
Mainly because I wanted something like this for a project I was working on, but anything complete had yet to be made (in python)


Quick Start
-------------

To install, get the library directly from PyPI:

.. code-block::

   $ pip install swagrinth

Getting up and running is easy

.. code-block:: python3

   import swagrinth

   # Client is used to interact with modrinth's database
   client = Client()
   
   the_project = client.get('project', 'sodium')
   print(the_project.slug) # Prints 'sodium'

You can't access some things without providing a valid token

.. code-block:: python3

   authed_client = Client('your-epic-token')

or

.. code-block:: python3

   authed_client = Client()
   authed_client.set_auth('your-epic-token')


Help & Issues
-------------

I'm in the Modrinth Discord server, so shoot me a ping if you have any questions or concerns.

If you think this module is crap, you are 100% correct now go away.


.. toctree::
   :maxdepth: 2
   :hidden:

   Client
   ClassBehavior


.. toctree::
   :hidden:
   :caption: Data Classes

   



Project
SearchResult
ProjectListing
Version
VersionFile
Dependency
DependencyList

User
Team
TeamMember

License
ModMessage
Image
DonationSite
Notification


