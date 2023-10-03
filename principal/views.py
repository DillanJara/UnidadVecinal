from django.shortcuts import render, redirect, HttpResponse
from .forms.form_juntaVecinos import *
from .forms.form_personas import *
import hashlib
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def verHome(request):
    if request.session.get("errorLogin"):
        del request.session["errorLogin"]
        request.session.modified = True
    return render(request, "home.html")

def verLogin(request):
    return render(request, "login.html")

def validarLogin(request):
    try:
        v_email = request.POST.get('correo')
        v_password = hashlib.sha256(request.POST.get('password').encode())
        password_encriptada = v_password.hexdigest()
        miembro = Miembro.objects.get(mie_correo=v_email, mie_password=password_encriptada)
        if miembro.mie_estado == "Habilitado":
            del request.session["errorLogin"]
            request.session.modified = True
            request.session['correo'] = miembro.mie_correo
            request.session['rut'] = miembro.mie_rut
            return redirect('/index/'+ str(miembro.mie_rut))
        else:
            request.session["errorLogin"] = "Su cuenta aun se encuentra deshabilitada"
            return redirect("/login")
    except:
        request.session["errorLogin"] = "Correo o contraseña invalidos. Intente de nuevo"
        return redirect("/login")

def cerrarSesion(request):
    del request.session['correo']
    del request.session['rut']
    request.session.modified=True
    return redirect('/')

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
    if Miembro.objects.get(junta_vecinos_jun_id=jun_id, cargo_car_id=1):
        return HttpResponse("Esta junta de vecinos ya tiene a su presidente registrado")
    else:
        if form.is_valid():
            password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
            password_encriptada = password_encriptada.hexdigest()
            Miembro.objects.create(
                mie_rut              = request.POST['mie_rut'],
                mie_dv               = request.POST['mie_dv'],
                mie_nombre           = request.POST['mie_nombre'],
                mie_ap_paterno       = request.POST['mie_ap_paterno'],
                mie_ap_materno       = request.POST['mie_ap_materno'],
                mie_fecha_nacimiento = request.POST.get('mie_fecha_nacimiento'),
                mie_telefono         = request.POST['mie_telefono'],
                mie_correo           = request.POST['mie_correo'],
                mie_password         = password_encriptada,
                mie_direccion        = request.POST['mie_direccion'],
                junta_vecinos_jun_id = jun_id,
                mie_estado           = "Habilitado",
                cargo_car_id         = 1
            )
            return redirect("/")
    context = {
        "juntaVecinos" : juntaVecinos,
        "cargo"        : cargo,
        "form"         : form
    }
    return render(request, "registrarPresidente.html", context)

def registrarMiembro(request):
    form         = AgregarMiembro(request.POST or None)
    juntaVecinos = JuntaVecinos.objects.all()
    cargo        = Cargo.objects.get(car_id=4)
    if form.is_valid():
            password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
            password_encriptada = password_encriptada.hexdigest()
            Miembro.objects.create(
                mie_rut              = request.POST['mie_rut'],
                mie_dv               = request.POST['mie_dv'],
                mie_nombre           = request.POST['mie_nombre'],
                mie_ap_paterno       = request.POST['mie_ap_paterno'],
                mie_ap_materno       = request.POST['mie_ap_materno'],
                mie_fecha_nacimiento = request.POST.get('mie_fecha_nacimiento'),
                mie_telefono         = request.POST['mie_telefono'],
                mie_correo           = request.POST['mie_correo'],
                mie_password         = password_encriptada,
                mie_direccion        = request.POST['mie_direccion'],
                junta_vecinos_jun_id = JuntaVecinos.objects.get(jun_nombre=request.POST['mie_junta_vecinos']).jun_id,
                mie_estado           = "Deshabilitado",
                cargo_car_id         = 4
            )
            return redirect("/")
    context = {
        "juntaVecinos" : juntaVecinos,
        "cargo"        : cargo,
        "form"         : form
    }
    return render(request, "registroMiembro.html", context)

def verIndex(request, rut):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=rut)
        miembrosDeshabilitados = Miembro.objects.filter(junta_vecinos_jun_id=miembro.junta_vecinos_jun_id, mie_estado="Deshabilitado")
        familiarMiembro = FamiliarMiembro.objects.filter(miembro_mie_id=rut)
        form = agregarFamiliarMiembro(request.POST or None)
        context = {
            "miembro": miembro,
            "miembrosDeshabilitados": miembrosDeshabilitados,
            "familiarMiembro": familiarMiembro, 
            "form":  form
        }
        if form.is_valid():
            FamiliarMiembro.objects.create(
                fam_mie_rut        = request.POST["fam_mie_rut"],
                fam_mie_dv         = request.POST["fam_mie_dv"],
                fam_mie_nombre     = request.POST["fam_mie_nombre"],
                fam_mie_ap_paterno = request.POST["fam_mie_ap_paterno"],
                fam_mie_ap_materno = request.POST["fam_mie_ap_materno"],
                fam_mie_telefono   = request.POST["fam_mie_telefono"],
                fam_mie_parentesco = request.POST["fam_mie_parentesco"],
                miembro_mie_id     = miembro.mie_rut
            )
            return redirect('/index/'+ str(miembro.mie_rut))
        return render(request, "index.html", context)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

def eliminarFamiliarMiembro(request, fam_mie_rut):
    if request.session.get("correo"):
        familiarMiembro = FamiliarMiembro.objects.get(fam_mie_rut=fam_mie_rut)
        FamiliarMiembro.delete(familiarMiembro)
        return redirect("/index/" + str(request.session.get("rut")))
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
    
def activarCuenta(request, mie_rut):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=mie_rut)
        miembro.mie_estado = "Habilitado"
        miembro.save()
        asunto = "Activacion cuenta " + miembro.junta_vecinos_jun.jun_nombre
        cuerpo = "Le informamos que su cuenta iniciada en Unidad Vecinal fue activada, ya puede iniciar sesion."
        message = EmailMultiAlternatives(asunto, cuerpo, settings.EMAIL_HOST_USER, [miembro.mie_correo]) 
        message.send()
        return redirect("/index/" + str(request.session.get("rut")))
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
