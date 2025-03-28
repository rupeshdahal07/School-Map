from django.contrib import admin
from .models import School, Facility
# Register your models here.
admin.site.register(School)
admin.site.register(Facility)
# Compare this snippet from SchoolMap/api/models.py: