from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
# -------------------------------------------------------
from principal.models import JuntaVecinos, Miembro
# Create your views here.

@login_required(login_url='/administracion/accounts/login/')
def inicio(request):
    contexto = {
        'juntaVecinos': JuntaVecinos.objects.all(),
        'miembro': Miembro.objects.filter(cargo_car_id=1)
    }
    return render(request, 'inicio.html', contexto)


def salir(request):
    logout(request)
    return redirect('/administracion/accounts/login/')

@login_required(login_url='/administracion/accounts/login/')
def deshabilitarJunta(request, mie_rut, jun_id):
    miembro = Miembro.objects.get(mie_rut=mie_rut)
    juntaVecinos = JuntaVecinos.objects.get(jun_id=jun_id)

    miembro.mie_estado = "Deshabilitado"
    juntaVecinos.jun_habilitada = False
    # -------------------------------------------------------
    subject = 'INFORMACION IMPORTANTE PARA:' + juntaVecinos.jun_nombre
    message = "Sr./Sra. " + miembro.mie_nombre + " " + miembro.mie_ap_paterno + ", " + miembro.cargo_car.car_nombre + " de la junta de vecinos " + juntaVecinos.jun_nombre + ", le informamos que su cuenta y su junta de vecinos han sido DESACTIVADAS, comunicarse al correo remitente para mÁs información."
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [miembro.mie_correo, juntaVecinos.jun_correo])
    # -------------------------------------------------------
    email.send()
    # -------------------------------------------------------
    miembro.save()
    juntaVecinos.save()
    return redirect('/administracion/inicio/')

@login_required(login_url='/administracion/accounts/login/')
def habilitarJunta(request, mie_rut, jun_id):
    miembro = Miembro.objects.get(mie_rut=mie_rut)
    juntaVecinos = JuntaVecinos.objects.get(jun_id=jun_id)
    # -------------------------------------------------------
    miembro.mie_estado = "Habilitado"
    juntaVecinos.jun_habilitada = True
    # -------------------------------------------------------
    subject = 'INFORMACION IMPORTANTE PARA:' + juntaVecinos.jun_nombre
    message = "Sr./Sra. " + miembro.mie_nombre + " " + miembro.mie_ap_paterno + ", " + miembro.cargo_car.car_nombre + " de la junta de vecinos " + juntaVecinos.jun_nombre + ", le informamos que los datos de su junta ha sido validados correctamente, por lo tanto, su cuenta se ha ACTIVADO, ya puede ingresar a nuestra aplicacion con sus credenciales."
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [miembro.mie_correo, juntaVecinos.jun_correo])
    # -------------------------------------------------------
    email.send()
    # -------------------------------------------------------
    miembro.save()
    juntaVecinos.save()
    return redirect('/administracion/inicio/')

@login_required(login_url='/administracion/accounts/login/')
def rechazarJunta(request, mie_rut, jun_id):
    miembro = Miembro.objects.get(mie_rut=mie_rut)
    juntaVecinos = JuntaVecinos.objects.get(jun_id=jun_id)
    # -------------------------------------------------------
    miembro.mie_estado = "Deschabilitado"
    juntaVecinos.jun_habilitada = False
    # -------------------------------------------------------
    subject = 'INFORMACION IMPORTANTE PARA:' + juntaVecinos.jun_nombre
    message = "Sr./Sra. " + miembro.mie_nombre + " " + miembro.mie_ap_paterno + ", " + miembro.cargo_car.car_nombre + " de la junta de vecinos " + juntaVecinos.jun_nombre + ", le informamos que los datos de su junta NO se VALIDARON correctamente, contactarse al correo remitente para la correccion de los datos."
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [miembro.mie_correo, juntaVecinos.jun_correo])
    # -------------------------------------------------------
    email.send()
    # -------------------------------------------------------
    miembro.save()
    juntaVecinos.save()
    return redirect('/administracion/inicio/')