from django.urls import include
from django.urls import path
from id_process.apps import IdProcessConfig


app_name = IdProcessConfig.name

urlpatterns = [
    path('api/', include('id_process.api.urls'), name='id-process-api'),
]
