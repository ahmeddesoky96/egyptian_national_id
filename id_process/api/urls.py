from django.urls import include
from django.urls import path


urlpatterns = [
    path('v1/', include('id_process.api.v1.urls'), name='id-process-api-v1'),
]
