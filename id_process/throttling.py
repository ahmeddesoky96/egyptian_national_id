from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


class APIKeyRateThrottle(BaseThrottle):
    
    def allow_request(self, request, view):
        if not hasattr(request, 'auth') or not request.auth:
            return False
            
        api_key = request.auth
        cache_key = f"throttle_api_key_{api_key.key}"
        
        now = timezone.now()
        requests = cache.get(cache_key, [])
        
        cutoff = now - timedelta(hours=1)
        requests = [req_time for req_time in requests if req_time > cutoff]
        
        if len(requests) >= 10:
            return False
        
        requests.append(now)
        cache.set(cache_key, requests, 3600) 
        return True
    
    def wait(self):
        return 3600  
    
