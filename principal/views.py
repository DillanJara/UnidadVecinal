from django.shortcuts import render, redirect, HttpResponse
from .forms import *
import hashlib

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
        return redirect("/registrarPresidente/" + str(junta_vecinos.jun_id))
    context = {
            "form": form, 
            "comunas": Comuna.objects.all()
        }
    return render(request, "registrarJunta.html", context)

def registrarPresidente(request, jun_id):
    form         = AgregarPresidente(request.POST or None)
    juntaVecinos = JuntaVecinos.objects.get(jun_id=jun_id)
    cargo        = Cargo.objects.get(car_id = 1)

    if form.is_valid():
        password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
        password_encriptada = password_encriptada.hexdigest()
        Miembro.objects.create(
            mie_rut              = request.POST['mie_rut'],
            mie_dv               = request.POST['mie_dv'],
            mie_nombre           = request.POST['mie_nombre'],
            mie_ap_paterno       = request.POST['mie_ap_paterno'],
            mie_ap_materno       = request.POST['mie_ap_materno'],
            mie_fecha_nacimiento  = request.POST.get('mie_fecha_nacimiento'),
            mie_telefono         = request.POST['mie_telefono'],
            mie_correo           = request.POST['mie_correo'],
            mie_password         = password_encriptada,
            mie_direccion        = request.POST['mie_direccion'],
            junta_vecinos_jun_id = jun_id,
            mie_estado           = "Habilitado",
            cargo_car_id         = 1
        )
        return redirect("/")
        #return HttpResponse("rut:" + str(request.POST['mie_rut']))

    context = {
        "juntaVecinos" : juntaVecinos,
        "cargo"        : cargo,
        "form"         : form
    }
    return render(request, "registrarPresidente.html", context)


