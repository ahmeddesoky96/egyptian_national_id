from rest_framework import serializers


class NationalIDValidationSerializer(serializers.Serializer):
    national_id = serializers.CharField()
    
    def validate_national_id(self, value):
        if not value:
            raise serializers.ValidationError("National ID is required")
        return value
