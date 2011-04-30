from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    file_id = models.BigIntegerField()
    last_changed = models.DateTimeField()
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __unicode__(self):
        return self.title