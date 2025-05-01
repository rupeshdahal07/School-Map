
from django.contrib import admin
from .models import School, Facility
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        # You can specify which fields to import/export
        # fields = ('name', 'province', 'district', 'address', 'latitude', 'longitude', 'school_type')
        # Or import all fields

            # Note: If you want to skip unchanged records, set `skip_unchanged` to True                  
            # and `report_skipped` to False. This will prevent unchanged records from being reported in the import/export report.
        fields = '__all__'
        skip_unchanged = True
        report_skipped = False

class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource
    list_display = ('name', 'district', 'province', 'school_type')
    list_filter = ('province', 'district', 'school_type')
    search_fields = ('name', 'address')

admin.site.register(School, SchoolAdmin)
admin.site.register(Facility)