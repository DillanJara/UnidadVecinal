from django import forms
from ..models import *
import re

class AgregarEspacio(forms.ModelForm):
    class Meta:
        model = Espacio
        exclude = ["junta_vecinos_jun", "esp_imagen", ]

    esp_nombre = forms.CharField(max_length=30, label="Nombre Espacio")
    esp_direccion = forms.CharField(max_length=50, label="Direccion")
    esp_telefono = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })

    def clean_esp_telefono(self):
        esp_telefono = self.cleaned_data.get('esp_telefono')
        patron = r"^\+569\d{8}$"
        if bool(re.match(patron, esp_telefono)):
            return esp_telefono
        else:
            raise forms.ValidationError("El formato del numero debe ser +56 9 1234 5678")