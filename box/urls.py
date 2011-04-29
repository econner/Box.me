from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^box/', include('box.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^login/?$', 'box.users.views.box_login'),
    (r'^nlp/?$', 'box.suggestion_engine.views.do_analysis'),
    (r'^search/', include('haystack.urls')),
    (r'^sugg/', 'box.suggestion_engine.views.get_similar_docs'),
)
