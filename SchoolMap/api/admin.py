from django.contrib import admin
from .models import School, Facility
# Register your models here.

class SchoolAdmin(admin.ModelAdmin):
     list_display = ('name', 'district', 'address', 'phone') 
admin.site.register(School)
admin.site.register(Facility)
# Compare this snippet from SchoolMap/api/models.py: