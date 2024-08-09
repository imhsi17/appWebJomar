from django.db import models

# Create your models here.

class Alumno(models.Model):
    
    id =  models.AutoField(primary_key=True, blank=False, null=False, )
    dni = models.CharField('Dni', max_length=8)
    apellido_nombre = models.CharField('Apellidos y Nombres', max_length=250)
    grado = models.CharField('Grado', max_length=12)
    seccion = models.CharField('Sección', max_length=1)
        
    def __str__(self) -> str:
        
        return f"{self.apellido_nombre}."

class Asistencia(models.Model):
    
    id = models.AutoField(primary_key=True, blank=False, null=False)
    fecha_registro = models.DateField('Fecha')
    hora_registro = models.TimeField('Hora')
    alumno = models.CharField('Apellidos y Nombres', max_length=250)
    dni_almn = models.CharField('Dni', max_length=8)
    grado = models.CharField('Grado', max_length=12)
    seccion = models.CharField('Sección',max_length=1)
        
    def __str__(self) -> str:
        
        return f"{self.alumno}: {self.fecha_registro} / {self.hora_registro}"

