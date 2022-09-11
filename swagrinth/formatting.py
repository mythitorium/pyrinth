'''
Formatting.py

Centralized place for defining how data classes are dynamically initialized


NOTE
Hey listen up future me, so you don't fuck up on some stupid shit like formatting in the future
Which I know you will otherwise because you'll stop working on this for 4 weeks to play fucking minecraft and watch youtube 

1. Corrections vars: {'expected payload key' : 'replacement key'} <- Make sure the replacement key is what is listed in the respective blueprint var
2. Blueprint vars: {'key' : 'default value & expected type'} 
    - Make sure all class references are in strings, _build takes care of it
    - Handling arrays is simple: put <default value & expected type> inside of a array

There ya go dumbass have fun
'''


FIX_PROJECT = {'updated' : 'modified_at', 'published' : 'created_at', 'approved' : 'approved_at'}
BP_PROJECT = {                            #
    'id' : '',                            #
    'slug' : '',                          #
    'title' : '',                         #
    'description' : '',                   #
    'body' : '',                          #
    'client_side' : '',                   #
    'server_side' : '',                   #

    'catagories': [''],                   #
    'additional_categories' : [''],       #
    
    'issues_url' : '',                    #
    'source_url' : '',                    #
    'wki_url' : '',                       #
    'discord_url' : '',                   #

    'donation_urls' : ['DonationSite'],   #
    'project_type' : '',                  #
    'downloads' : 0,                      #
    'followers' : 0,                      #
    'icon_url' : '',                      #
    'team_id' : '',                       #

    'moderator_message' : 'ModMessage',   #
    'created_at' : '',                    # 
    'modified_at' : '',                   #
    'approved_at' : '',                   #

    'license': {},                        #
    'versions' : [''],                   #
    'gallery': [{}],                      #
}

BP_DONATION_SITE = {
    'id' : '',                            #
    'platform' : '',                      #
    'url' : '',                           #
}

BP_MOD_MESSAGE = {
    'message' : '',                       #
    'body' : '',                          #
}

FIX_USER = {'created' : 'created_at', 'name' : 'display_name'}
BP_USER = {
    'username' : '',                      #
    'display_name' : '',                  #
    'email' : '',                         #
    'bio' : '',                           #
    'id' : '',                            #
    'github_id' : 0,                      #
    'avatar_url' : '',                    #
    'created_at' : '',                    #
    'role' : '',                          #
}

BP_TEAM = {
    'members' : ['TeamMember']            #
}

FIX_TEAM_MEMBER = {'permissions' : 'perms'}
BP_TEAM_MEMBER = {
    'team_id' : '',                       #
    'user' : 'User',                      #
    'role' : '',                          #
    'perms' : 0,                          #
    'accepted' : False                    #
}

FIX_NOTIFICATION = {'created' : 'created_at', 'text' : 'body', 'link' : 'url'}
BP_NOTIFICATION = {
    'id' : '',                            #
    'user_id' : '',                       #
    'type' : '',                          #
    'title' : '',                         #
    'body' : '',                          #
    'url' : '',                           #
    'read' : False,                       #
    'created_at' : ''                     #
    # NOTE: TO-DO Figure out and add 'actions'
}

FIX_VERSION = {'date_published' : 'created_at'}
BP_VERSION = {
    'name' : '',
    'version_number' : '',
    'changelog' : '',
    'dependencies' : ['Dependency'],
    'game_versions' : [''],
    'version_type' : '',
    'loaders' : [''],
    'is_featured' : False,
    'id' : '',
    'project_id' : '',
    'author_id' : '',
    'created_at' : '',
    'downloads' : 0,
    'files' : ['VersionFile']
}

FIX_VERSION_FILE = {'size' : 'file_size'}
BP_VERSION_FILE = {
    'hashes' : {},
    'url' : '',
    'name' : '',
    'primary' : False,
    'file_size' : 0,
}

FIX_DEPENDENCY = {'file_name' : 'name', 'dependency_type' : 'type'}
BP_DEPENDENCY = {
    'version_id' : '',
    'project_id' : '',
    'name' : '',
    'type' : '',
}