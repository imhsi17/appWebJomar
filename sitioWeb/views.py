from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from sitioWeb.models import *

#Importaciones extras
from babel.dates import format_date
from datetime import datetime
import locale
from sitioWeb import utils

#Login de la página de inicio
def login_docente(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/reportes')
        else:
            messages.error(request, "Credenciales Incorrectas. Intentelo Nuevamente.")
    return render(request, "login_docentes.html")

#Cerrar sesión desde la página de inicio
def salir(request):
    logout(request)
    return redirect('/')

#Permite visualizar la asistencia de un alumno buscandola con su dni.
#URL: asistencia_alumno/
def buscar_asistencia(request):
    
    mensajes = []
    if request.method == 'POST':
        dni = request.POST.get('dni_alumno')
        alumno = Alumno.objects.filter(dni=dni)
        if alumno:
            asist = Asistencia.objects.filter(dni_almn=dni).order_by('-id')[:5]
            hora_limite = datetime.strptime("07:50:00", "%H:%M:%S").time()
            hora_inicio = datetime.strptime("07:00:00", "%H:%M:%S").time()
            context = {"alumno":alumno, "asistencias":asist, "hora_limite":hora_limite, "hora_inicio":hora_inicio}
            return render(request, "mostrar_asistencia.html", context)
        else:
            mensajes.append("DNI INCORRECTO")
            context = {"mensajes":mensajes}
            return render(request, "buscar_asistencia.html", context)
            
    return render(request, "buscar_asistencia.html")

#Página de inicio
def inicio(request):
    
    return render(request, "inicio.html")

#Muestra los alumnos registrados al filtrarlos por grado y sección
def lista_alumnos(request):
    
    if request.method == "POST":
        grado = request.POST.get('grado')
        seccion = request.POST.get('seccion')
        
        alumnos = Alumno.objects.filter(grado__icontains=grado, seccion__icontains=seccion).order_by('apellido_nombre')
        if alumnos:
            context = {"alumnos":alumnos, "grado":grado, "seccion":seccion}
            return render(request, "lista_alumnos.html", context)
        else:
            mensaje = "SIN ALUMNOS REGISTRADOS"
            context = {"mensaje":mensaje, "grado":grado, "seccion":seccion}
            return render(request, "lista_alumnos.html", context)
    
    return render(request, "lista_alumnos.html")

#Página de asistencias
def asistencias(request):
    
    return render(request, "asistencias.html")

#Muestra las asistencias registradas al filtrarlas por grado y sección
def lista_asistencias(request):
    
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        grado = request.POST.get('grado')
        seccion = request.POST.get('seccion')
        asistencias = Asistencia.objects.filter(fecha_registro__icontains=fecha, grado__icontains=grado, seccion__icontains=seccion).order_by('alumno')
        
        if asistencias:
            context = {"asistencias":asistencias, "fecha":fecha, "grado":grado, "seccion":seccion}
            return render(request, "asistencias_salon.html", context)
        
        else:
            mensaje = "SIN ASISTENCIAS REGISTRADAS"
            context = {"asistencias":asistencias, "fecha":fecha, "grado":grado, "seccion":seccion, "mensaje":mensaje}
            return render(request, "asistencias_salon.html", context)
        
    return render(request, "asistencias_salon.html", context)

#Edita la hora de una asistencia en base a su id.
def editar_asistencia(request, id):
    
    asistencia = Asistencia.objects.get(id=id)
    context = {"asistencia":asistencia}
       
    return render(request, "editar_asistencia.html", context)

#Guarda los cambios hechos en la asistencia editada
def asistencia_editada(request):
    
    id = int(request.POST.get('id'))
    nueva_hora = request.POST.get('hora')
    
    asistencia = Asistencia.objects.get(id=id)
    asistencia.hora_registro = nueva_hora
    asistencia.save()
    messages.success(request, "Asistencia editada correctamente.")
    
    return redirect('/asistencias/')

#Página para generar reportes
def reportes(request):
    
    return render(request, "reportes.html")

#Genera el reporte de asistencias del día por salón
def generar_reporte(request):
    
    locale.setlocale(locale.LC_TIME, 'es_PE.UTF-8')
    fecha = datetime.now().strftime('%Y-%m-%d')
    fecha = request.POST.get('fecha')
    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
    fecha_archivo = format_date(fecha_date, format='full', locale='es')
    grado = request.POST.get('grado')
    seccion = request.POST.get('seccion')
    hora_tarde = request.POST.get('hora_tarde')
    alumnos = Alumno.objects.filter(grado=grado, seccion=seccion).order_by('apellido_nombre')
    asistencias = {}
    for alumno in alumnos:
        dni = alumno.dni
        nombre = alumno.apellido_nombre
        asistencia = Asistencia.objects.get(fecha_registro=fecha, dni_almn=dni)
        asistencias[str(nombre)] = asistencia.hora_registro
    
    context = {"asistencias":asistencias, "grado":grado, "seccion":seccion,
                 "tarde":hora_tarde, "fecha":fecha_archivo}

    pdf = utils.render_pdf("modelo_reporte.html", context)
    nombre_archivo = str(grado) +"_"+ str(seccion) +" "+ str(fecha)
    pdf['Content-Disposition'] = f'attachment; filename={nombre_archivo}.pdf'
    return pdf

#Genera un resumen del día en base a las asistencias registradas
def resumen_reporte(request):
    
    locale.setlocale(locale.LC_TIME, 'es_PE.UTF-8')
    fecha = datetime.now().strftime('%Y-%m-%d')
    fecha = request.POST.get('fecha')
    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
    fecha_archivo = format_date(fecha_date, format='full', locale='es')
    hora_inicio = "07:00:00"
    hora_tarde = request.POST.get('hora_tarde')
    hora_final = "12:00:00"
    grados = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
    secciones = ["A", "B", "C", "D", "E", "F", "G"]
    alumnos = []
    registros = []
    asistencias_puntuales = []
    asistencias_tarde = []
    faltas = []
    sumatoria_alumnos = []
    sumatoria_registros = []
    sumatoria_puntuales = []
    sumatoria_faltas = []
    sumatoria_tardes = []
    for grado in grados:
        suma_alumnos = 0
        suma_registros = 0
        suma_puntuales = 0
        suma_faltas = 0
        suma_tardes = 0
        for seccion in secciones:
            n_alumno = Alumno.objects.filter(grado__icontains=grado, seccion__icontains=seccion)
            n_registros = Asistencia.objects.filter(grado__icontains=grado,
                                                    seccion__icontains=seccion,
                                                    fecha_registro__icontains=fecha)
            n_puntuales = Asistencia.objects.filter(grado__icontains=grado,
                                                    seccion__icontains=seccion,
                                                    fecha_registro__icontains=fecha,
                                                    hora_registro__range=(hora_inicio, hora_tarde))
            n_tarde = Asistencia.objects.filter(grado__icontains=grado, seccion__icontains=seccion,
                                                fecha_registro__icontains=fecha,
                                                hora_registro__range=(hora_tarde, hora_final))
            n_faltas = Asistencia.objects.filter(grado__icontains=grado, seccion__icontains=seccion, 
                                                 fecha_registro__icontains=fecha, hora_registro="00:00:00")
            faltas.append(len(n_faltas))
            asistencias_puntuales.append(len(n_puntuales))
            asistencias_tarde.append(len(n_tarde))
            n_registros = len(n_registros) - len(n_faltas)
            registros.append(n_registros)
            alumnos.append(len(n_alumno))
            suma_alumnos = suma_alumnos + len(n_alumno)
            suma_registros = suma_registros + n_registros
            suma_puntuales = suma_puntuales + len(n_puntuales)
            suma_faltas = suma_faltas + len(n_faltas)
            suma_tardes = suma_tardes + len(n_tarde)
        
        sumatoria_alumnos.append(suma_alumnos)
        sumatoria_registros.append(suma_registros)
        sumatoria_puntuales.append(suma_puntuales)
        sumatoria_tardes.append(suma_tardes)
        sumatoria_faltas.append(suma_faltas)
    
    sumatoria_total = []
    sumatoria_total.append(sum(sumatoria_alumnos))
    sumatoria_total.append(sum(sumatoria_registros))
    sumatoria_total.append(sum(sumatoria_puntuales))
    sumatoria_total.append(sum(sumatoria_faltas))
    sumatoria_total.append(sum(sumatoria_tardes))
    
    context = {"fecha":fecha_archivo, "alumnos":alumnos, "registros":registros, "puntuales":asistencias_puntuales,
               "tarde":asistencias_tarde, "faltas":faltas, "suma_alumnos":sumatoria_alumnos, "suma_registros":sumatoria_registros,
               "suma_puntuales":sumatoria_puntuales, "suma_tardes":sumatoria_tardes, "suma_faltas":sumatoria_faltas,
               "sumatoria_total":sumatoria_total}
    
    pdf = utils.render_pdf("resumen_reporte.html", context)
    nombre_archivo = "Cuadro Resumen " + str(fecha)
    pdf['Content-Disposition'] = f'attachment; filename={nombre_archivo}.pdf'
    return pdf

#Elimina un alumno en base a su id
def eliminar_alumno(request, id):
    
    alumno = Alumno.objects.get(id=id)
    nombre = alumno.apellido_nombre
    alumno.delete()
    messages.warning(request, f"{nombre} Eliminado.")
    return redirect('/')

#Edita el nombre y sección de un alumno en base a su id
def editar_alumno(request, id):
    
    alumno = Alumno.objects.get(id=id)
    context = {'alumno':alumno}
    return render(request, "editar_alumno.html", context)

#Guarda los cambios hechos del alumno editado
def alumno_editado(request):
    
    id = int(request.POST.get('id'))
    nuevo_nombre = request.POST.get('apellido_nombre')
    nueva_seccion = request.POST.get('seccion')
    
    alumno = Alumno.objects.get(id=id)
    alumno.apellido_nombre = nuevo_nombre
    alumno.seccion = nueva_seccion
    alumno.save()
    messages.success(request, "Alumno editado correctamente.")
    
    return redirect('/')

