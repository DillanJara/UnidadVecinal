"""UnidadVecinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from principal.views import *

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('', verHome, name="home"),
    #-------------------------------------------------------------------------
    path('administracion/', include('administracion.urls')),
    path('api/', include('rest_api.urls')),
    #-------------------------------------------------------------------------
    path('login/', verLogin, name="login"),
    path('validarLogin', validarLogin, name="validarLogin"),
    path('cerrarSesion', cerrarSesion, name="cerrarSesion"),
    #-------------------------------------------------------------------------
    path('encontrarCuenta', encontrarCuenta, name="encontrarCuenta"),
    path('errorEncontrarCuenta', errorEncontrarCuenta, name="errorEncontrarCuenta"),
    path('cambiarPassword/<int:mie_rut>', cambiarPassword, name="cambiarPassword"),
    #-------------------------------------------------------------------------
    path('registrarMiembro/', registrarMiembro, name="registrarMiembro"),
    path('registrarJuntaVecinos/', registrarJunta, name="registrarJuntaVecinos"),
    path('registrarPresidente/<int:jun_id>', registrarPresidente, name="registrarPresidente"),
    #-------------------------------------------------------------------------
    path('index/<int:rut>', verIndex, name="index"),
    path('verPerfil/<int:mie_rut>', verPerfil, name="verPerfil"),
    #-------------------------------------------------------------------------
    path('agregarFamiliar/', agregarFamiliarMiembro, name="agregarFamiliar"),
    path('eliminarFamiliarMiembro/<int:fam_mie_rut>', eliminarFamiliarMiembro, name="eliminarFamiliarMiembro"),
    path('modificarFamiliarMiembro/<int:fam_mie_rut>', modificarFamiliarMiembro, name="modificarFamiliarMiembro"),
    #-------------------------------------------------------------------------
    path('activarCuenta/<int:mie_rut>', activarCuenta, name="activarCuenta"),
    path('visualizarMiembros/', visualizarMiembros, name="visualizarMiembros"),
    path('cambiarCargo/<int:mie_rut>/<int:car_id>', cambiarCargo, name="cambiarCargo"),
    path('eliminarMiembro/<int:mie_rut>', eliminarMiembro, name="eliminarMiembro"),
    #-------------------------------------------------------------------------
    path('enviarAviso', enviarAvisos, name="enviarAviso"),
    #-------------------------------------------------------------------------
    path('obtenerCertificado/<int:mie_rut>/<int:cer_id>', obtenerCetificado, name="obtenerCertificado"),
    path("obtenerCertificadoAsistencia/<int:asis_id>", obtenerCertificadoAsistencia, name="obtenerCertificadoAsistencia"),
    path('verSolicitudes/<int:mie_rut>', verSolicitudes, name="verSolicitudes"),
    #-------------------------------------------------------------------------
    path('agregarProyecto/', agregarProyecto, name="agregarProyecto"),
    path('verProyectos/', verProyectos, name="verProyectos"),
    path('cambiarEstadoProyecto/<int:proy_id>/<int:est_proy_id>', cambiarEstadoProyecto, name="cambiarEstadoProyecto"),
    #-------------------------------------------------------------------------
    path('agregarEspacios/', agregarEspacios, name="agregarEspacios"),
    path('verEspacios/', verEspacios, name="verEspacios"),
    #-------------------------------------------------------------------------
    path('agregarReserva/<int:esp_id>', agregarReserva, name="agregarReserva"),
    path('detalleReserva/<int:res_id>', detalleReserva, name="detalleReserva"),
    path('verReservas/<int:mie_rut>', verReservas, name="verReservas"),
    #-------------------------------------------------------------------------
    path('registrarFirma/<int:mie_rut>', firma, name="registraFirma"),
    #-------------------------------------------------------------------------
    path('agregarNoticia/', agregarNoticia, name="agregarNoticia"),
    path('verNoticias/', verNoticias, name="verNoticias"),
    path('detalleNoticia/<int:not_id>', detalleNoticia, name="detalleNoticia"),
    #-------------------------------------------------------------------------
    path('verCuotas/', verCuotas, name="verCuotas"),
    path('procesar-pago/', procesarPago, name='procesar_pago'),
    path('stripe_webhook', stripe_webhook, name='stripe_webhook'),
    path('pagoRealizado/', pagoRealizado, name="pagoRealizado"),
    path('verPagos/', verPagos, name='verPagos'),
    #-------------------------------------------------------------------------
    path('agregarActividad/', agregarActividades, name="agregarActividad"),
    path('verActividades/', verActividades, name="verActividades"),
    path('detalleActividad/<int:act_id>', detalleActividad, name="detalleActividad"),
    #-------------------------------------------------------------------------
    path('detalleAsistencia/<int:asis_id>', detalleAsistencia, name="detalleAsistencia"),
    path('verAsistencias/', verAsistencias, name="verAsistencias")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)