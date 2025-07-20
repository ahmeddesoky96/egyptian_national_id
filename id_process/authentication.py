from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from id_process.models import APIAuthentication
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone


class APIUser(AnonymousUser):

    def __init__(self, api_key):
        self.api_key = api_key
        
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class APIAuth(BaseAuthentication):

    def authenticate(self, request):
        api_key = self.get_api_key_from_request(request)
        if not api_key:
            return None
            
        try:
            key_obj = APIAuthentication.objects.select_related('user').get(
                key=api_key, 
                is_active=True
            )
            key_obj.last_used = timezone.now()
            key_obj.save(update_fields=['last_used'])
            
            return (APIUser(key_obj), key_obj)
        except APIAuthentication.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
    
    def get_api_key_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('ApiKey '):
            return auth_header[7:]
        
        return request.META.get('HTTP_API_KEY')