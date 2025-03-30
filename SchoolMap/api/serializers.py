from rest_framework import serializers
from .models import School, Facility

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']

class SchoolSerializer(serializers.ModelSerializer):
    facilities = serializers.SerializerMethodField()
    
    def get_facilities(self, obj):
        return list(obj.facilities.values_list('name', flat=True))
    
    def get_google_maps_url(self, obj):
        return obj.get_google_maps_url
    
    class Meta:
        model = School
        fields = '__all__'
