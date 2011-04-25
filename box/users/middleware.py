from boxdotnet import BoxDotNet
from django.conf import settings

class BoxMiddleware(object):
    def process_request(self, request):
        """
        Attempt to get the auth token from the box api.
        """
        
        return None