from django.urls import path
from . import views

urlpatterns = [
    path('validarCertificado/<sol_cer_id>/<mie_rut>', views.validarCertificado, name="validarCertificado"),
]