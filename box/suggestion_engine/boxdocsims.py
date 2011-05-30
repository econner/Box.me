from boxdotnet import BoxDotNet

# take a user, and search his files for a given query - HA
def box_search_file(profile, query, api_key):
	box = BoxDotNet()
	searchFiles = box.get_search(api_key, profile.token, query)
	return searchFiles

def box_preview(fileid, profile, api_key):
    box = BoxDotNet()
    folder_id = box.get_folder_id(fileid, profile.token, api_key)
    preview_url = 'https://www.box.net/files#/files/0/f/%s/1/f_%s' % (folder_id, fileid)
    return preview_url