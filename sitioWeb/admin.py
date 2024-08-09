from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources
from sitioWeb.models import *

# Register your models here.

class Alumno_resource(resources.ModelResource):
    class Meta:
        
        model = Alumno

class Asistencia_resource(resources.ModelResource):
    
    class Meta:
        
        model = Asistencia

class Alumno_admin(ImportExportModelAdmin, admin.ModelAdmin):
    
    list_display = ("apellido_nombre", "grado", "seccion", "dni")
    list_filter = ("grado", "seccion")
    search_fields = ("apellido_nombre",)
    resource_class = Alumno_resource

class Asistencia_admin(ImportExportModelAdmin, admin.ModelAdmin):
    
    list_display = ("alumno", "fecha_registro", "hora_registro")
    list_filter = ("grado", "seccion")
    resource_class = Asistencia_resource


admin.site.register(Alumno, Alumno_admin)
admin.site.register(Asistencia, Asistencia_admin)
