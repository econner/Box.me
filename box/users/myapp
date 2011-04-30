from django.db import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    token = models.CharField(max_length=255, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.token)
    
    def authenticate(self):
        return authenticate(token=self.token)
