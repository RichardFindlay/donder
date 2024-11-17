from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import mountain

# Register your models here.
@admin.register(mountain)

# allow db fields additions through admin
class MountainAdmin(ImportExportModelAdmin):
    pass