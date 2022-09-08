'''
Formatting.py

Centralized place for defining how data classes are dynamically initialized
'''


FIX_PROJECT = {'updated' : 'modified_at', 'published' : 'created_at', 'approved' : 'approved_at'}
BP_PROJECT = {
    'id' : '',                        #
    'slug' : '',
    'title' : '', 
    'description' : '',
    'body' : '',
    'client_side' : '', 
    'server_side' : '',

    'catagories': [{}],
    'additional_categories' : [{}],

    'issues_url' : '',
    'source_url' : '',
    'wki_url' : '',
    'discord_url' : '',

    'donation_urls' : ['DonationSite'],
    'project_type' : '',
    'downloads' : 0,
    'followers' : 0,
    'icon_url' : '',
    'team_id' : '',

    'moderator_message' : 'ModMessage',
    'created_at' : '',
    'modified_at' : '',
    'approved_at' : '',

    'license': {},
    'versions' : [str],
    'gallery': [{}],
}

BP_DONATION_SITE = {
    'id' : '',
    'platform' : '',
    'url' : '',
}

BP_MOD_MESSAGE = {
    'message' : '',
    'body' : '',
}

FIX_USER = {'created' : 'created_at', 'name' : 'display_name'}
BP_USER = {
    'username' : '',
    'display_name' : '',
    'email' : '',
    'bio' : '',
    'id' : '',
    'github_id' : 0,
    'avatar_url' : '',
    'created_at' : '',
    'role' : '',
}
