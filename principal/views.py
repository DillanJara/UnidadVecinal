from django.shortcuts import render, redirect, HttpResponse
from .forms.juntaVecinos import *
from .forms.miembro import *
from .forms.familiarMiembro import *
from .forms.proyecto import *
from .forms.espacios import *
from .forms.reservas import *
import hashlib
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, time, timedelta


# Create your views here.

def verHome(request):
    if request.session.get("errorLogin"):
        del request.session["errorLogin"]
        request.session.modified = True
    if request.session.get("correo"):
        del request.session["correo"]
        del request.session['rut']
        request.session.modified = True
    if request.session.get("alertaLogin"):
        del request.session["alertaLogin"]
    return render(request, "home.html")


def verLogin(request):
    return render(request, "login.html")


def validarLogin(request):
    try:
        email = request.POST.get('correo')
        password = hashlib.sha256(request.POST.get('password').encode())
        password_encriptada = password.hexdigest()
        miembro = Miembro.objects.get(
            mie_correo=email, mie_password=password_encriptada)
        if miembro.mie_estado == "Habilitado":
            if request.session.get("errorLogin"):
                del request.session["errorLogin"]
            request.session.modified = True
            request.session['correo'] = miembro.mie_correo
            request.session['rut'] = miembro.mie_rut
            return redirect('/index/' + str(miembro.mie_rut))
        else:
            request.session["errorLogin"] = "Su cuenta aun se encuentra deshabilitada"
            return redirect("/login")
    except:
        request.session["errorLogin"] = "Correo o contraseña invalidos. Intente de nuevo"
        return redirect("/login")


def cerrarSesion(request):
    del request.session['correo']
    del request.session['rut']
    request.session.modified = True
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
    return render(request, "registroJunta/registrarJunta.html", context)


def registrarPresidente(request, jun_id):
    form         = AgregarPresidente(request.POST or None)
    juntaVecinos = JuntaVecinos.objects.get(jun_id=jun_id)
    cargo        = Cargo.objects.get(car_id=1)
    if Miembro.objects.filter(junta_vecinos_jun_id=jun_id, cargo_car_id=1).count() > 0:
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
            return redirect("/registrarFirma")
    context = {
        "juntaVecinos": juntaVecinos,
        "cargo": cargo,
        "form": form
    }
    return render(request, "registroJunta/registrarPresidente.html", context)


def registrarMiembro(request):
    form = AgregarMiembro(request.POST or None)
    juntaVecinos = JuntaVecinos.objects.all()
    cargo = Cargo.objects.get(car_id=4)
    if form.is_valid():
        password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
        password_encriptada = password_encriptada.hexdigest()
        Miembro.objects.create(
            mie_rut=request.POST['mie_rut'],
            mie_dv=request.POST['mie_dv'],
            mie_nombre=request.POST['mie_nombre'],
            mie_ap_paterno=request.POST['mie_ap_paterno'],
            mie_ap_materno=request.POST['mie_ap_materno'],
            mie_fecha_nacimiento=request.POST.get('mie_fecha_nacimiento'),
            mie_telefono=request.POST['mie_telefono'],
            mie_correo=request.POST['mie_correo'],
            mie_password=password_encriptada,
            mie_direccion=request.POST['mie_direccion'],
            junta_vecinos_jun_id=JuntaVecinos.objects.get(
                jun_nombre=request.POST['mie_junta_vecinos']).jun_id,
            mie_estado="Deshabilitado",
            cargo_car_id=4
        )
        return redirect("/")
    context = {
        "juntaVecinos": juntaVecinos,
        "cargo": cargo,
        "form": form
    }
    return render(request, "registroJunta/registroMiembro.html", context)


def verIndex(request, rut):
    if request.session.get("correo"):
        if request.session.get("errorValidarRut"):
            del request.session["errorValidarRut"]
            request.session.modified = True
        # ------------------------------------------------------
        miembro                = Miembro.objects.get(mie_rut=rut)
        miembrosDeshabilitados = Miembro.objects.filter(junta_vecinos_jun_id=miembro.junta_vecinos_jun_id, mie_estado="Deshabilitado")
        familiarMiembro        = FamiliarMiembro.objects.filter(miembro_mie_id=rut)
        proyectos              = Proyecto.objects.filter(miembro_mie_id=miembro.mie_rut)
        form                   = agregarFamiliarMiembro(request.POST or None)
        miembrosRegistrados    = Miembro.objects.filter(junta_vecinos_jun_id=miembro.junta_vecinos_jun_id).count()
        miembrosActivos        = Miembro.objects.filter(junta_vecinos_jun_id=miembro.junta_vecinos_jun_id, mie_estado="Habilitado").count()
        # ------------------------------------------------------
        context = {
            "miembro"                : miembro,
            "miembrosDeshabilitados" : miembrosDeshabilitados,
            "familiarMiembro"        : familiarMiembro,
            "form"                   : form,
            "proyectos"              : proyectos,
            "miembrosRegistrados": miembrosRegistrados,
            "miembrosActivos": miembrosActivos
        }
        # ------------------------------------------------------
        if form.is_valid():
            if validar_rut(request.POST["fam_mie_rut"], request.POST["fam_mie_dv"]):
                if request.session.get("errorValidarRut"):
                    del request.session["errorValidarRut"]
                    request.session.modified = True
                FamiliarMiembro.objects.create(
                    fam_mie_rut=request.POST["fam_mie_rut"],
                    fam_mie_dv=request.POST["fam_mie_dv"],
                    fam_mie_nombre=request.POST["fam_mie_nombre"],
                    fam_mie_ap_paterno=request.POST["fam_mie_ap_paterno"],
                    fam_mie_ap_materno=request.POST["fam_mie_ap_materno"],
                    fam_mie_telefono=request.POST["fam_mie_telefono"],
                    fam_mie_parentesco=request.POST["fam_mie_parentesco"],
                    miembro_mie_id=miembro.mie_rut
                )
                return redirect('/index/' + str(miembro.mie_rut))
            else:
                request.session["errorValidarRut"] = "El digito verificador del Rut ingresado no es valido"
        return render(request, "principal/index.html", context)
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


def modificarFamiliarMiembro(request, fam_mie_rut):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        familiarMiembro = FamiliarMiembro.objects.get(fam_mie_rut=fam_mie_rut)
        form = editarFamiliarMiembro(instance=familiarMiembro)
        context = {
            "miembro": miembro,
            "familiarMiembro": familiarMiembro,
            "form": form
        }
        if request.method == "POST":
            familiarMiembro.fam_mie_nombre = request.POST["fam_mie_nombre"]
            familiarMiembro.fam_mie_ap_paterno = request.POST["fam_mie_ap_paterno"]
            familiarMiembro.fam_mie_ap_materno = request.POST["fam_mie_ap_materno"]
            familiarMiembro.fam_mie_telefono = request.POST["fam_mie_telefono"]
            familiarMiembro.fam_mie_parentesco = request.POST["fam_mie_parentesco"]
            familiarMiembro.miembro_mie_rut = miembro.mie_rut
            familiarMiembro.save()
            return redirect("/index/" + str(request.session.get("rut")))
        return render(request, "principal/modificarFamiliarMiembro.html", context)
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
        message = EmailMultiAlternatives(
            asunto, cuerpo, settings.EMAIL_HOST_USER, [miembro.mie_correo])
        message.send()
        return redirect("/index/" + str(request.session.get("rut")))
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def visualizarMiembros(request):
    if request.session.get("correo"):
        miembro        = Miembro.objects.get(mie_rut=request.session.get("rut"))
        miembros       = Miembro.objects.filter(junta_vecinos_jun_id=miembro.junta_vecinos_jun_id)
        cargos         = Cargo.objects.exclude(car_id=1)
        contexto = {
            "miembro" : miembro,
            "miembros"       : miembros,
            "cargos"         : cargos
        }
        return render(request, "principal/visualizarMiembros.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def cambiarCargo(request, mie_rut, car_id):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=mie_rut)
        cargo = Cargo.objects.get(car_id=car_id)
        miembro.cargo_car = cargo
        miembro.save()
        return redirect("/visualizarMiembros")
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def obtenerCetificado(request, mie_rut, cer_id):
    miembro     = Miembro.objects.get(mie_rut=request.session.get("rut"))
    certificado = Certificado.objects.get(cer_id=cer_id)
    presidente  = Miembro.objects.get(cargo_car_id=1, junta_vecinos_jun_id=miembro.junta_vecinos_jun_id)
    # ------------------------------------------------------
    solicitud = SolicitudCertificado()
    solicitud.certificado_cer = certificado
    solicitud.miembro_mie = miembro
    # ------------------------------------------------------
    if certificado.cer_id == 1:
        if Miembro.objects.filter(mie_rut=mie_rut).count() > 0:
            solicitante = Miembro.objects.get(mie_rut=mie_rut)
            template = get_template("certificados/cert_residencia.html")
        else:
            solicitante = FamiliarMiembro.objects.get(fam_mie_rut=mie_rut)
            solicitud.sol_cer_familiar = True
            solicitud.sol_cer_rut_familiar = solicitante.fam_mie_rut
            template = get_template("certificados/cert_residencia_familiar.html")
    else:
        solicitante = miembro
        template = get_template("certificados/cert_socio.html")
    # ------------------------------------------------------
    solicitud.save()
    # ------------------------------------------------------
    context = {
        "solicitante" : solicitante,
        "miembro"     : miembro,
        "presidente"  : presidente,
        "certificado" : certificado,
        "solicitud"   : solicitud
    }
    # ------------------------------------------------------
    asunto = "Solicitud de " + certificado.cer_nombre
    cuerpo = miembro.mie_nombre + " " + miembro.mie_ap_materno + " le informamos que en su cuenta se ha realizado la solicitud de un " + certificado.cer_nombre + ". El certificado se descargó directamente en el dispositivo."
    message = EmailMultiAlternatives(asunto, cuerpo, settings.EMAIL_HOST_USER, [miembro.mie_correo])
    message.send()
    # ------------------------------------------------------
    html = template.render(context)
    # ------------------------------------------------------
    response = HttpResponse(content_type='application/pdf')
    if certificado.cer_id == 1:
        response['Content-Disposition'] = 'attachment; filename="Certificado_Residencia.pdf"'
    else:
        response['Content-Disposition'] = 'attachment; filename="Certificado_Socio.pdf"'
    # ------------------------------------------------------
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('No se pudo descargar tu certificado')
    return response


def agregarProyecto(request):
    if request.session.get("correo"):
        form = AgregarProyecto(request.POST or None)
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        if request.method == "POST":
            estado_proyecto = EstadoProyecto.objects.get(est_proy_estado="En Revision")
            Proyecto.objects.create(
                proy_nombre = request.POST["proy_nombre"],
                proy_descripcion = request.POST["proy_descripcion"],
                proy_imagen = request.FILES.get("proy_imagen"),
                estado_proyecto_est_proy = estado_proyecto,
                miembro_mie = miembro
            )
            return redirect("/index/" + str(request.session.get("rut")))
        context = {
            "form": form,
            "miembro": miembro
        }
        return render(request, "principal/proyecto/agregarProyecto.html", context)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def firma(request):
    if request.session.get("correo") or request.session.get("rut"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        if not request.session.get("correo") and request.session.get("rut"):
            del request.session["rut"]
            request.session.modified = True
        if request.method == 'POST':
            firma = request.POST["img"]
            miembro.mie_firma = firma
            miembro.save()
            return redirect("/index/" + str(request.session.get("rut")))
        contexto = {
            "miembro": miembro
        }
        return render(request, "principal/registrarFirma.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def verSolicitudes(request, mie_rut):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=mie_rut)
        solicitudes = SolicitudCertificado.objects.filter(miembro_mie=miembro)
        familiares = FamiliarMiembro.objects.filter(miembro_mie=miembro)
        contexto = {
            "miembro": miembro,
            "solicitudes": solicitudes,
            "familiares": familiares,
        }
        return render(request, "certificados/solicitudes/solicitudes_certificados.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

def agregarEspacios(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        form = AgregarEspacio(request.POST or None)
        contexto = {
            "form": form,
            "miembro": miembro
        }
        if request.method == "POST":
            Espacio.objects.create(
                esp_nombre = request.POST["esp_nombre"],
                esp_direccion = request.POST["esp_direccion"],
                esp_telefono  = request.POST["esp_telefono"],
                esp_imagen = request.FILES.get("esp_imagen"),
                junta_vecinos_jun = miembro.junta_vecinos_jun
            )
            return redirect("/index/" + str(request.session.get("rut")))
        return render(request, "principal/espacios/agregarEspacios.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def verEspacios(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        espacios = Espacio.objects.filter(junta_vecinos_jun=miembro.junta_vecinos_jun)
        contexto = {
            "miembro": miembro,
            "espacios": espacios
        }
        return render(request, "principal/espacios/verEspacios.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def agregarReserva(request,  esp_id):
    miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
    espacio = Espacio.objects.get(esp_id=esp_id)
    form = AgregarReserva(request.POST or None)
    # ------------------------------------------------------
    contexto = {
        "form": form,
        "miembro": miembro,
        "espacio": espacio
    }
    # ------------------------------------------------------
    if request.method == "POST":
        if form.is_valid():
            reservas_existente = Reserva.objects.filter(
                miembro_mie=miembro,
                res_fecha=request.POST["res_fecha"]
            )
            reservas_existente_2 = Reserva.objects.filter(
                espacio_esp     = espacio,
                res_fecha       = request.POST["res_fecha"],
                res_hora_inicio = time.fromisoformat(request.POST["res_hora_inicio"])
            )
            if reservas_existente.exists():
                contexto["error"] = True
                return render(request, "principal/reservas/agregarReservas.html", contexto)
            # ------------------------------------------------------
            elif reservas_existente_2.exists():
                contexto["error2"] = True
                return render(request, "principal/reservas/agregarReservas.html", contexto)
            # ------------------------------------------------------
            else:
                reserva = Reserva()
                reserva.res_fecha = request.POST["res_fecha"]
                reserva.res_hora_inicio = time.fromisoformat(request.POST["res_hora_inicio"])
                reserva.res_hora_fin = (datetime.combine(datetime.min, reserva.res_hora_inicio) + timedelta(hours=1)).time()
                reserva.espacio_esp = espacio
                reserva.miembro_mie = miembro
                reserva.save()
                return redirect("/detalleReserva/" + str(reserva.res_id))
    return render(request, "principal/reservas/agregarReservas.html", contexto)

def detalleReserva(request, res_id):
    reserva = Reserva.objects.get(res_id=res_id)
    miembro = reserva.miembro_mie
    contexto = {
        "reserva": reserva,
        "miembro": miembro
    }
    return render(request, "principal/reservas/detalleReserva.html", contexto)
