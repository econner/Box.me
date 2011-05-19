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
    (r'^login/?$', 'box.users.views.box_login'),
    
    (r'^/?$', 'box.icebox.views.index'),
    # mobwrite views
    (r'^sync/?$', 'box.icebox.views.sync'), 
    (r'^editor/?$', 'box.icebox.views.editor'), 
    (r'^save_note/?$', 'box.icebox.views.save_note'), 
    (r'^note/(?P<id>\d+)/?$', 'box.icebox.views.note'),
    
    (r'^search/', 'box.suggestion_engine.views.get_similar_docs'),
    (r'^nlp/?$', 'box.suggestion_engine.views.do_analysis'),
    
    # this is used for the search box interface provided by haystack

#    (r'^search/', include('haystack.urls')),

	# search/download/version history stuff
	(r'^profile/?$', 'box.users.views.box_search_file'),
	(r'^download/?$', 'box.users.views.box_download_file'),
	(r'^versions/?$', 'box.users.views.box_versions'),

    (r'^search/', include('haystack.urls')),
    

)

# static content served only in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.PROJECT_ROOT}),
    )