from django.shortcuts import render, redirect
from .forms import *

# Create your views here.

def verIndex(request):
    return render(request, "index.html")

def verLogin(request):
    return render(request, "login.html")

def registrarMiembro(request):
    return render(request, "registroMiembro.html")

def verHome(request):
    return render(request, "home.html")

def registrarJunta(request):
    if request.method == 'GET':
        context = {
            "form": AgregarJuntaVecinos()
        }

        return render(request, "registrarJunta.html", context)
    elif request.method == 'POST':
        form = AgregarJuntaVecinos(request.POST)
        if form.is_valid():
            # Aquí los datos del formulario ya están validados
            # Puedes crear una instancia de JuntaVecinos y asignar la comuna correctamente
            junta_vecinos = form.save(commit=False)
            nombre_comuna = form.cleaned_data['comuna_com_id']  # Obtén la comuna seleccionada en el formulario
            comuna = Comuna.objects.get(com_nombre=nombre_comuna)  # Obtén la instancia de Comuna
            junta_vecinos.comuna_com_id = comuna  # Asigna la comuna a la JuntaVecinos
            junta_vecinos.save()  # Guarda la instancia de JuntaVecinos en la base de datos

            return redirect("/")
