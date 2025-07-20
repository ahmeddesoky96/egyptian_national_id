from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from id_process.authentication import APIAuth
import time
from django.utils import timezone
from rest_framework import status
from id_process.serializers import NationalIDValidationSerializer
from id_process.validators import NationalIDValidator
from id_process.models import APICallLog


class ValidateNationalIDView(APIView):
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        start_time = time.time()
        
        serializer = NationalIDValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        national_id = serializer.validated_data['national_id']
        
        is_valid, validation_result = NationalIDValidator.validate(national_id)
        
        processing_time = int((time.time() - start_time) * 1000) 
        
        response_data = {
            'is_valid': is_valid
        }
        
        if is_valid:
            response_data['extracted_data'] = validation_result['extracted_data']
        else:
            response_data['errors'] = validation_result['errors']
        
        self.track_api_call(
            request=request,
            national_id=national_id,
            is_valid=is_valid,
            response_data=response_data,
            processing_time=processing_time
        )
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def track_api_call(self, request, national_id, is_valid, response_data, processing_time):
        try:
            APICallLog.objects.create(
                api_auth=request.auth,
                endpoint='validate-id',
                national_id=national_id,  
                is_valid=is_valid,
                extracted_data=response_data,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                processing_time_ms=processing_time
            )
        except Exception as e:
            print(f"Error tracking API call: {e}")
