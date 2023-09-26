from django.shortcuts import render, redirect, HttpResponse
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
    form = AgregarJuntaVecinos(request.POST or None)

    if form.is_valid():
        junta_vecinos = form.save(commit=False)
        comuna = Comuna.objects.get(com_nombre=request.POST['jun_comuna'])
        junta_vecinos.jun_correo = request.POST['jun_correo']
        junta_vecinos.comuna_com_id = comuna.com_id
        junta_vecinos.save()
        return redirect("/")
    context = {
            "form": form, 
            "comunas": Comuna.objects.all()
        }
    return render(request, "registrarJunta.html", context)


