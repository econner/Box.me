from django.db import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    token = models.CharField(max_length=255, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.token)
    
    def authenticate(self):
        return authenticate(token=self.token)


# Here's the model:
# TEMP MODEL FOR DEMO
class Message(models.Model):
    msg = models.TextField('Message')
    timestamp = models.DateTimeField('Timestamp', auto_now_add=True)
    posted_by = models.CharField(max_length=50)