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
    path('eliminarFamiliarMiembro/<int:fam_mie_rut>', eliminarFamiliarMiembro, name="eliminarFamiliarMiembro"),
    path('modificarFamiliarMiembro/<int:fam_mie_rut>', modificarFamiliarMiembro, name="modificarFamiliarMiembro"),
    path('activarCuenta/<int:mie_rut>', activarCuenta, name="activarCuenta"),
    path('visualizarMiembros/', visualizarMiembros, name="visualizarMiembros"),
    path('cambiarCargo/<int:mie_rut>/<int:car_id>', cambiarCargo, name="cambiarCargo"),
    #-------------------------------------------------------------------------
    path('obtenerCertificado/<int:mie_rut>/<int:cer_id>', obtenerCetificado, name="obtenerCertificado"),
    path('verSolicitudes/<int:mie_rut>', verSolicitudes, name="verSolicitudes"),
    #-------------------------------------------------------------------------
    path("agregarProyecto/", agregarProyecto, name="agregarProyecto"),
    #-------------------------------------------------------------------------
    path("agregarEspacios/", agregarEspacios, name="agregarEspacios"),
    path("verEspacios/", verEspacios, name="verEspacios"),
    #-------------------------------------------------------------------------
    path("agregarReserva/<int:esp_id>", agregarReserva, name="agregarReserva"),
    path('detalleReserva/<int:res_id>', detalleReserva, name="detalleReserva"),
    #-------------------------------------------------------------------------
    path("registrarFirma/", firma, name="registraFirma"),
    #-------------------------------------------------------------------------
    path("agregarNoticia", agregarNoticia, name="agregarNoticia"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)