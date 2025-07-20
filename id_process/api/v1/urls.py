from django.urls import include
from django.urls import path
from django.conf import settings
from rest_framework import routers
from id_process.views import ValidateNationalIDView

urlpatterns = [
    path('validate-id/', ValidateNationalIDView.as_view(), name='validate_national_id'),
]
