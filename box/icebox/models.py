from django.db import models
from users.models import *

class UserListField(models.CommaSeparatedIntegerField):
    """
    List of users that can be associated with a model.  This object
    knows how to populate itself with user objects and serialize itself
    for entry into the database.
    """
    __metaclass__ = models.SubfieldBase
    description = "A list of User ids that can be stored and retrieved with a model"

    def to_python(self, value):
        if not value:
            return [ ]
        
        if isinstance(value, list):
            return value

        # if value is a comma separated list still
        users = [User.objects.get(pk=uid) for uid in value.split(",")]
        return users

    def get_prep_value(self, value):
        if not value:
            return ""
            
        if not isinstance(value, list):
            # already a comma separated list
            return value 

        ids = [str(user.id) for user in value]
        ids.sort()
        return ",".join(ids)

class Note(models.Model):
    """
    Store every note created by a user in the database.
    These will be mirrored on Box.net, but we hit our database
    first for intermediate caching.
    """
    creator = models.ForeignKey(User)
    collaborators = UserListField(max_length=500) # need a max length since we subclass CommaSeparatedIntegerField
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    revision = models.IntegerField(default=0)   # revision number of this note

    def __unicode__(self):
        return self.title
