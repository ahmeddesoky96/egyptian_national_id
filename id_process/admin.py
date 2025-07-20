from django.contrib import admin
from id_process.models import APIAuthentication, APICallLog

@admin.register(APIAuthentication)
class APIAuthenticationAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'is_active', 'created_at', 'last_used')
    list_filter = ('is_active', 'created_at')
    search_fields = ('key', 'user__username')
    readonly_fields = ('key', 'created_at', 'last_used')
    

@admin.register(APICallLog)
class APICallLogAdmin(admin.ModelAdmin):
    list_display = ('api_auth', 'endpoint', 'national_id', 'is_valid', 'timestamp', 'processing_time_ms')
    list_filter = ('is_valid', 'endpoint', 'timestamp')
    search_fields = ('national_id', 'api_auth__name')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  