from django.db import models
from django.contrib.auth.models import User
import uuid


class BaseTrackModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        
class APIAuthentication(BaseTrackModel):
    key = models.CharField(max_length=64, unique=True)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='api_user')
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['key', 'user']),
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_key():
        return str(uuid.uuid4()).replace('-', '')


class APICallLog(BaseTrackModel):
    api_auth = models.ForeignKey(APIAuthentication, on_delete=models.RESTRICT, related_name='call')
    endpoint = models.CharField(max_length=100, null=True, blank=True)
    national_id = models.CharField(max_length=14, null=True, blank=True)  
    is_valid = models.BooleanField()
    extracted_data = models.JSONField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    processing_time_ms = models.IntegerField(null=True, blank=True)  
    
    class Meta:
        indexes = [
            models.Index(fields=['api_auth', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"Call to {self.endpoint} at {self.timestamp}"

