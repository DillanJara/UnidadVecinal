from django.urls import path, include
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicioAdministracion'),
    path('accounts/', include('django.contrib.auth.urls'), name='loginAdministracion'),
    path('salir/', views.salir, name='salir'),
    path('deshabilitarJunta/<int:mie_rut>/<int:jun_id>/', views.deshabilitarJunta, name='deshabilitarJunta'),
    path('habilitarJunta/<int:mie_rut>/<int:jun_id>/', views.habilitarJunta, name='habilitarJunta'),
    path('rechazarJunta/<int:mie_rut>/<int:jun_id>/', views.rechazarJunta, name='rechazarJunta'),
]