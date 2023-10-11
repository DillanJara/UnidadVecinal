from django import forms
from ..models import *

class AgregarProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = ["estado_proyecto_est_proy", "miembro_mie", "proy_imagen", ]

    proy_nombre = forms.CharField(label="Nombre del Proyecto", max_length=30)
    proy_descripcion = forms.CharField(label="Agregue una descripcion", widget=forms.Textarea())