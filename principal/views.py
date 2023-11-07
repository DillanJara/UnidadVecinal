from django.shortcuts import render, redirect, HttpResponse
from .forms.juntaVecinos import *
from .forms.miembro import *
from .forms.familiarMiembro import *
from .forms.proyecto import *
from .forms.espacios import *
from .forms.reservas import *
from .forms.noticias import *
from .forms.actividades import *
import hashlib
import stripe
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, time, timedelta
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# ------------------------------------------------------
# seccion de inicio
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
        request.session.modified = True
    return render(request, "home.html")
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de autenticacion
def verLogin(request):
    contexto = {
        "form": AgregarMiembro(request.POST or None)
    }
    return render(request, "login.html", contexto)


def errorEncontrarCuenta(request):
    return render(request, "recuperarPassword/errorEncontrarCuenta.html")


def encontrarCuenta(request):
    mie_rut = request.POST["mie_rut"]
    mie_dv = request.POST["mie_dv"]
    mie_correo = request.POST["mie_correo"]
    if Miembro.objects.filter(mie_rut=mie_rut, mie_dv=mie_dv, mie_correo=mie_correo).exists():
        miembro = Miembro.objects.get(mie_rut=mie_rut, mie_dv=mie_dv, mie_correo=mie_correo)
        return redirect("cambiarPassword/" + str(miembro.mie_rut))
    else:
        return redirect("/errorEncontrarCuenta")


def cambiarPassword(request, mie_rut):
    if request.session.get("errorLogin"):
        del request.session["errorLogin"]
        request.session.modified = True
    miembro = Miembro.objects.get(mie_rut=mie_rut)
    contexto = {
        "miembro": miembro,
        "form": AgregarMiembro(request.POST or None)
    }
    if request.method == "POST":
        password = hashlib.sha256(request.POST.get('mie_password').encode())
        password_encriptada = password.hexdigest()
        miembro.mie_password = password_encriptada
        miembro.save()
        asunto = "Cambio de contraseña"
        cuerpo = miembro.mie_nombre + " " + miembro.mie_ap_paterno + " le informamos que su en cuenta se ha realizado una actualizacion de la contraseña"
        message = EmailMultiAlternatives(asunto, cuerpo, settings.EMAIL_HOST_USER, [miembro.mie_correo])
        message.send()
        return redirect('/login')
    return render(request, "recuperarPassword/cambiarPassword.html", contexto)


def validarLogin(request):
    try:
        email               = request.POST.get('correo')
        password            = hashlib.sha256(request.POST.get('password').encode())
        password_encriptada = password.hexdigest()
        miembro             = Miembro.objects.get(mie_correo=email, mie_password=password_encriptada)
        # ------------------------------------------------------
        if miembro.mie_estado == "Habilitado":
            if request.session.get("errorLogin"):
                del request.session["errorLogin"]
            # ------------------------------------------------------
            request.session.modified  = True
            request.session['correo'] = miembro.mie_correo
            request.session['rut']    = miembro.mie_rut
            # ------------------------------------------------------
            return redirect('/index/' + str(miembro.mie_rut))
        elif not miembro.junta_vecinos_jun.jun_habilitada:
            request.session["errorLogin"] = "Aun no se valida la vericidad de su Junta Vecinal"
            return redirect("/login")
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
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de registro
def registrarJunta(request):
    form = AgregarJuntaVecinos(request.POST or None)
    if form.is_valid():
        junta_vecinos                          = form.save(commit=False)
        comuna                                 = Comuna.objects.get(com_nombre=request.POST['jun_comuna'])
        junta_vecinos.comuna_com_id            = comuna.com_id
        # ------------------------------------------------------
        junta_vecinos.jun_directiva            = request.POST['directiva1'] + ", " + request.POST['directiva2'] + ", " + request.POST['directiva3']
        junta_vecinos.jun_certificado_vigencia = request.FILES.get("jun_certificado_vigencia")
        junta_vecinos.save()
        # ------------------------------------------------------
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
    # ------------------------------------------------------
    if Miembro.objects.filter(junta_vecinos_jun_id=jun_id, cargo_car_id=1).count() > 0:
        return HttpResponse("Esta junta de vecinos ya tiene a su presidente registrado")
    else:
        if form.is_valid():
            password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
            password_encriptada = password_encriptada.hexdigest()
            # ------------------------------------------------------
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
                mie_estado           = "Deshabilitado",
                cargo_car_id         = 1,
                mie_documento        = request.FILES.get("mie_documento")
            )
            return redirect("/registrarFirma/" + str(request.POST['mie_rut']))
    # ------------------------------------------------------
    context = {
        "juntaVecinos": juntaVecinos,
        "cargo": cargo,
        "form": form
    }
    return render(request, "registroJunta/registrarPresidente.html", context)


def firma(request, mie_rut):
    miembro = Miembro.objects.get(mie_rut=mie_rut)
    if request.method == 'POST':
        firma             = request.POST["img"]
        miembro.mie_firma = firma
        miembro.save()
        # ------------------------------------------------------
        if request.session.get("rut"):
            return redirect("/index/" + str(request.session.get("rut")))
        return render(request, "registroJunta/mensajeRegistro.html")
    # ------------------------------------------------------
    contexto = {
        "miembro": miembro
    }
    return render(request, "registroJunta/registrarFirma.html", contexto)


def registrarMiembro(request):
    form         = AgregarMiembro(request.POST or None)
    juntaVecinos = JuntaVecinos.objects.all()
    cargo        = Cargo.objects.get(car_id=4)
    # ------------------------------------------------------
    if form.is_valid():
        password_encriptada = hashlib.sha256(request.POST['mie_password'].encode())
        password_encriptada = password_encriptada.hexdigest()
        # ------------------------------------------------------
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
            junta_vecinos_jun_id=JuntaVecinos.objects.get(jun_nombre=request.POST['mie_junta_vecinos']).jun_id,
            mie_estado="Deshabilitado",
            cargo_car_id=4
        )
        return redirect("/")
    # ------------------------------------------------------
    context = {
        "juntaVecinos": juntaVecinos,
        "cargo": cargo,
        "form": form
    }
    return render(request, "registroJunta/registroMiembro.html", context)
# ------------------------------------------------------


# ------------------------------------------------------
# seccion principal
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
                # ------------------------------------------------------
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


def verPerfil(request, mie_rut):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=mie_rut)
        contexto = {
            "miembro": miembro
        }
        return render(request, "principal/verPerfil.html", contexto)
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
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de gestion de miembros
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
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de certificados
def obtenerCetificado(request, mie_rut, cer_id):
    if request.session.get("correo"):
        miembro     = Miembro.objects.get(mie_rut=request.session.get("rut"))
        certificado = Certificado.objects.get(cer_id=cer_id)
        presidente  = Miembro.objects.get(cargo_car_id=1, junta_vecinos_jun_id=miembro.junta_vecinos_jun_id)
        # ------------------------------------------------------
        if SolicitudCertificado.objects.filter(sol_cer_fecha=timezone.now().date(), miembro_mie=miembro).count() > 3:
            return render(request, "certificados/error_solicitud.html")
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
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def verSolicitudes(request, mie_rut):
    if request.session.get("correo"):
        miembro     = Miembro.objects.get(mie_rut=mie_rut)
        solicitudes = SolicitudCertificado.objects.filter(miembro_mie=miembro)
        familiares  = FamiliarMiembro.objects.filter(miembro_mie=miembro)
        # ------------------------------------------------------
        contexto = {
            "miembro": miembro,
            "solicitudes": solicitudes,
            "familiares": familiares,
        }
        # ------------------------------------------------------
        return render(request, "certificados/solicitudes/solicitudes_certificados.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de proyectos
def agregarProyecto(request):
    if request.session.get("correo"):
        form    = AgregarProyecto(request.POST or None)
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        # ------------------------------------------------------
        if request.method == "POST":
            estado_proyecto = EstadoProyecto.objects.get(est_proy_estado="En Revision")
            # ------------------------------------------------------
            Proyecto.objects.create(
                proy_nombre = request.POST["proy_nombre"],
                proy_descripcion = request.POST["proy_descripcion"],
                proy_imagen = request.FILES.get("proy_imagen"),
                estado_proyecto_est_proy = estado_proyecto,
                miembro_mie = miembro
            )
            return redirect("/index/" + str(request.session.get("rut")))
        # ------------------------------------------------------
        context = {
            "form": form,
            "miembro": miembro
        }
        # ------------------------------------------------------
        return render(request, "principal/proyecto/agregarProyecto.html", context)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

# REALIZAR
# REALIZAR
# REALIZAR
# REALIZAR
# REALIZAR REALIZAR
def verProyectos(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        proyectos = Proyecto.objects.filter(miembro_mie__junta_vecinos_jun=miembro.junta_vecinos_jun)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

# ------------------------------------------------------
# seccion de espacios y reservas
def agregarEspacios(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        form    = AgregarEspacio(request.POST or None)
        # ------------------------------------------------------
        contexto = {
            "form"    : form,
            "miembro" : miembro
        }
        # ------------------------------------------------------
        if request.method == "POST":
            Espacio.objects.create(
                esp_nombre = request.POST["esp_nombre"],
                esp_direccion = request.POST["esp_direccion"],
                esp_telefono  = request.POST["esp_telefono"],
                esp_imagen = request.FILES.get("esp_imagen"),
                junta_vecinos_jun = miembro.junta_vecinos_jun
            )
            # ------------------------------------------------------
            return redirect("/index/" + str(request.session.get("rut")))
        return render(request, "principal/espacios/agregarEspacios.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def verEspacios(request):
    if request.session.get("correo"):
        miembro  = Miembro.objects.get(mie_rut=request.session.get("rut"))
        espacios = Espacio.objects.filter(junta_vecinos_jun=miembro.junta_vecinos_jun)
        # ------------------------------------------------------
        contexto = {
            "miembro": miembro,
            "espacios": espacios
        }
        # ------------------------------------------------------
        return render(request, "principal/espacios/verEspacios.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def agregarReserva(request,  esp_id):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        espacio = Espacio.objects.get(esp_id=esp_id)
        form    = AgregarReserva(request.POST or None)
        # ------------------------------------------------------
        contexto = {
            "form"    : form,
            "miembro" : miembro,
            "espacio" : espacio
        }
        # ------------------------------------------------------
        if request.method == "POST":
            if form.is_valid():
                reservas_existente = Reserva.objects.filter(
                    miembro_mie = miembro,
                    res_fecha   = request.POST["res_fecha"]
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
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def detalleReserva(request, res_id):
    if request.session.get("correo"):
        reserva = Reserva.objects.get(res_id=res_id)
        miembro = reserva.miembro_mie
        # ------------------------------------------------------
        contexto = {
            "reserva": reserva,
            "miembro": miembro
        }
        return render(request, "principal/reservas/detalleReserva.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


# ------------------------------------------------------
# seccion de noticias
def agregarNoticia(request):
    if request.session.get("correo"):
        form    = AgregarNoticia(request.POST or None)
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        # ------------------------------------------------------# ------------------------------------------------------
        contexto = {
            "form"    : form,
            "miembro" : miembro
        }
        # ------------------------------------------------------
        if request.method == 'POST':
            noticia = Noticia()
            noticia.not_titulo      = request.POST["not_titulo"]
            noticia.not_subtitulo   = request.POST["not_subtitulo"]
            noticia.not_descripcion = request.POST["not_descripcion"]
            noticia.not_imagen      = request.FILES.get("not_imagen")
            noticia.miembro_mie     = miembro
            noticia.save()
            # ------------------------------------------------------
            return redirect("/verNoticias")
        return render(request, "principal/noticias/agregarNoticia.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def verNoticias(request):
    if request.session.get("correo"):
        miembro  = Miembro.objects.get(mie_rut=request.session.get("rut"))
        noticias = Noticia.objects.filter(miembro_mie__junta_vecinos_jun=miembro.junta_vecinos_jun)
        # ------------------------------------------------------
        contexto = {
            "miembro": miembro,
            "noticias": noticias
        }
        # ------------------------------------------------------
        return render(request, "principal/noticias/verNoticias.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def detalleNoticia(request, not_id):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get("rut"))
        noticia = Noticia.objects.get(not_id=not_id)
        contexto = {
            "miembro": miembro,
            "noticia": noticia
        }
        return render(request, "principal/noticias/detalleNoticia.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de pago de cuotas
def verCuotas(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        cuotas = CuotaSocial.objects.filter(miembro_mie=miembro)
        contexto = {
            'miembro': miembro,
            'cuotas': cuotas
        }
        return render(request, "principal/pago/verCuotas.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def procesarPago(request):
    if request.session.get("correo"):
        today = datetime.today()
        mesActual = today.month
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        if CuotaSocial.objects.filter(cuo_fecha_pago__month=mesActual, miembro_mie=miembro).count() > 0:
            return render(request, 'principal/pago/mensajePago.html', {"miembro": miembro})
        else:
            return redirect('https://buy.stripe.com/test_fZe03gbwZfqAdcQ8ww')
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
	return HttpResponse(status=200)

def pagoRealizado(request):
    if request.session.get("correo"):
        miembro                    = Miembro.objects.get(mie_rut=request.session.get('rut'))
        cuotaSocial                = CuotaSocial()
        cuotaSocial.cuo_monto      = 5000
        cuotaSocial.cuo_fecha_pago = datetime.today()
        cuotaSocial.cuo_estado     = 'Pagado'
        cuotaSocial.miembro_mie    = miembro
        cuotaSocial.save()
        contexto = {
            'miembro': miembro,
        }
        return render(request, "principal/pago/pago.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
# ------------------------------------------------------


# ------------------------------------------------------
# seccion de actividades
def agregarActividades(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        form = AgregarActividad(request.POST or None)
        contexto = {
            "miembro": miembro,
            "form": form
        }
        if request.method == 'POST':
            if form.is_valid:
                actividad = Actividad()
                actividad.act_fecha = request.POST["act_fecha"]
                actividad.act_descripcion = request.POST["act_descripcion"]
                actividad.act_cupo = request.POST["act_cupo"]
                if len(request.POST["act_cuota"]) == 0:
                    actividad.act_cuota = 0
                else:
                    actividad.act_cuota = request.POST["act_cuota"]
                actividad.tipo_actividad_tip_act = TipoActividad.objects.get(tip_act_id=request.POST["tipo_actividad_tip_act"])
                actividad.junta_vecinos_jun = miembro.junta_vecinos_jun
                actividad.save()
                return HttpResponse("actividad guardada")
        return render(request, "principal/actividades/registrarActividades.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

def verActividades(request):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        actividades = Actividad.objects.filter(junta_vecinos_jun=miembro.junta_vecinos_jun, act_fecha__gt=datetime.now())
        contexto = {
            "miembro": miembro,
            "actividades": actividades
        }
        return render(request, "principal/actividades/verActividades.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")


def detalleActividad(request, act_id):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        actividad = Actividad.objects.get(act_id=act_id)
        contexto = {
            "miembro": miembro,
            "actividad": actividad
        }
        if Asistencia.objects.filter(actividad_act=actividad, miembro_mie=miembro):
            contexto["validacionAsistencia"] = True
        if request.method == "POST":
            actividad.act_cupo = actividad.act_cupo - int(request.POST["cantidad_asistentes"])
            actividad.save()
            asistencia = Asistencia()
            asistencia.asis_cantidad = int(request.POST["cantidad_asistentes"])
            asistencia.miembro_mie = miembro
            asistencia.actividad_act = actividad
            asistencia.save()
            return redirect("detalleAsistencia/" + str(asistencia.asis_id))
        return render(request, "principal/actividades/detalleActividad.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")

def detalleAsistencia(request, asis_id):
    if request.session.get("correo"):
        miembro = Miembro.objects.get(mie_rut=request.session.get('rut'))
        asistencia = Asistencia.objects.get(asis_id=asis_id)
        contexto = { 
            "miembro": miembro,
            "asistencia": asistencia
        }
        return render(request, "principal/actividades/detalleasistencia.html", contexto)
    else:
        request.session["alertaLogin"] = "Debes iniciar sesion para usar la aplicacion"
        return redirect("/login")
# ------------------------------------------------------