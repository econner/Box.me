from boxdotnet import BoxDotNet

box = BoxDotNet()

# take a user, and search his files for a given query - HA
# Returns XMLNode of files in search results
# Returns None if no results found
def box_search_file(profile, query, api_key):
    return box.get_search(api_key, profile.token, query)

def box_preview(fileid, profile, api_key):
    folder_id = box.get_folder_id(fileid, profile.token, api_key)
    preview_url = 'https://www.box.net/files#/files/0/f/%s/1/f_%s' % (folder_id, fileid)
    return preview_url