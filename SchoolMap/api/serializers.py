from rest_framework import serializers
from .models import School, Facility

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']

class SchoolSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = '__all__'
