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
    (r'^nlp/?$', 'box.suggestion_engine.views.do_analysis'),
    (r'^/?$', 'box.users.views.index'),
    
    # mobwrite views
    (r'^sync/?$', 'box.users.views.sync'), 
    (r'^editor/?$', 'box.users.views.editor'), 
    
    (r'^search/', 'box.suggestion_engine.views.get_similar_docs'),
    
    # this is used for the search box interface provided by haystack
#    (r'^search/', include('haystack.urls')),

	# search/download/version history stuff
	(r'^profile/?$', 'box.users.views.box_search_file'),
	(r'^download/?$', 'box.users.views.box_download_file'),
	(r'^versions/?$', 'box.users.views.box_versions')	
)

# static content served only in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.PROJECT_ROOT}),
    )