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
