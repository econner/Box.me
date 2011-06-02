from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from models import UserProfile

class Auth(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class BoxAuth(Auth):
    def authenticate(self, box_user_id=None):
        try:
            return User.objects.get(username=box_user_id)
        except UserProfile.DoesNotExist:
            return None