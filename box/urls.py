from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
import os

urlpatterns = patterns('',
    # Example:
    # (r'^box/', include('box.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/?$', 'box.users.views.box_login', name="login"),
    
    url(r'^/?$', 'box.icebox.views.index', name="index"),
    # mobwrite views
    url(r'^sync/?$', 'box.icebox.views.sync', name="sync"), 
    url(r'^editor/?$', 'box.icebox.views.editor', name="editor"), 
    url(r'^activity/?$', 'box.icebox.views.activity', name="activity"), 
    url(r'^collaborators/?$', 'box.icebox.views.collaborators', name="collaborators"), 
    
    url(r'^ajax/save_note/?$', 'box.icebox.views.save_note', name="save_note"), 
    url(r'^ajax/add_collab/?$', 'box.icebox.views.add_collab', name="add_collab"),
    url(r'^ajax/search_collab/?$', 'box.icebox.views.search_collab', name="search_collab"),
    url(r'^ajax/del_collab/?$', 'box.icebox.views.del_collab', name="del_collab"),
    
    url(r'^note/(?P<id>\d+)/?$', 'box.icebox.views.note', name="note"),
    
    url(r'^docsims/?$', 'box.suggestion_engine.views.get_similar_docs', name="similar_docs"),
    url(r'^notesims/?$', 'box.suggestion_engine.views.get_similar_notes', name="similar_notes"),
    
    # this is used for the search box interface provided by haystack

#    (r'^search/', include('haystack.urls')),

	# search/download/version history stuff
	(r'^profile/?$', 'box.users.views.box_search_file'),
	(r'^download/?$', 'box.users.views.box_download_file'),
	(r'^versions/?$', 'box.users.views.box_versions'),
	(r'^keywords/?$', 'box.suggestion_engine.views.get_similar_docs'),

    (r'^search/', include('haystack.urls')),
    

)

# static content served only in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.PROJECT_ROOT}),
    )