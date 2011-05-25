from boxdotnet import BoxDotNet

# take a user, and search his files for a given query - HA
def box_search_file(profile, query, api_key):
	box = BoxDotNet()
	searchFiles = box.get_search(api_key, profile.token, query)
	return searchFiles
    
    
def box_download_file(auth_token, fileid):
    downloadurl = 'https://www.box.net/api/1.0/download/%s/%s' % (auth_token, fileid)
    return HttpResponseRedirect(downloadurl) # change