from rest_framework import viewsets
from .models import School
from .serializers import SchoolSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read, but only authenticated users can edit

    # Filtering by province, district, and municipality type
    def get_queryset(self):
        queryset = School.objects.all()
        province = self.request.query_params.get('province')
        district = self.request.query_params.get('district')
        municipality_type = self.request.query_params.get('municipality_type')
        school_type = self.request.query_params.get('school_type')

        if province:
            queryset = queryset.filter(province=province)
        if district:
            queryset = queryset.filter(district=district)
        if municipality_type:
            queryset = queryset.filter(municipality_type=municipality_type)
        if school_type:
            queryset = queryset.filter(school_type__icontains=school_type)

        return queryset

    @property
    def get_google_maps_url(self):
        """Generate a Google Maps URL based on coordinates or address."""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        elif self.address:
            # Format address for URL (replace spaces with +)
            formatted_address = self.address.replace(' ', '+')
            return f"https://www.google.com/maps?q={formatted_address}"
        return None