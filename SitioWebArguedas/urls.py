"""
URL configuration for SitioWebArguedas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from sitioWeb.views import *

#Para añadir nuevas URLS seguir la sintaxis mostrada
urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio_sesion/', login_docente),
    path('', inicio),
    path('asistencias/', asistencias),
    path('reportes/', reportes),
    path('lista_alumnos/', lista_alumnos),
    path('lista_asistencias/', lista_asistencias),
    path('editar_alumno/<int:id>', editar_alumno),
    path('alumno_editado/', alumno_editado),
    path('eliminar_alumno/<int:id>', eliminar_alumno),
    path('editar_asistencia/<int:id>', editar_asistencia),
    path('asistencia_editada/', asistencia_editada),
    path('generar_reporte/', generar_reporte),
    path('cuadro_resumen/', resumen_reporte),
    path('logout/', salir),
    path('asistencia_alumno/', buscar_asistencia),
]
