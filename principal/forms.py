from django import forms
from .models import *
import re

"""
class AgregarJuntaVecinos(forms.Form):
    jun_nombre = forms.CharField(label="Nombre de la Junta de Vecinos", max_length=50)
    jun_fecha_fundacion = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    jun_nombre_villa = forms.CharField(label="Nombre de la Unidad Territorial", max_length=50)
    jun_telefono = forms.CharField(label="Telefono", max_length=12)
    jun_correo = forms.EmailField(max_length=254)
    jun_direccion = forms.CharField(label="Direccion de Casa Central", max_length=100)
    jun_mision = forms.CharField(label="Mision", max_length=300, widget=forms.Textarea())
    comuna_com_id = forms.ModelChoiceField(queryset=Comuna.objects.all(), label="Comuna")
"""

class AgregarJuntaVecinos(forms.ModelForm):
    jun_nombre = forms.CharField(label="Nombre de la Junta de Vecinos", max_length=50)
    jun_fecha_fundacion = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), label="Fecha de fundacion")
    jun_nombre_villa = forms.CharField(label="Nombre de la Unidad Territorial", max_length=50)
    jun_telefono = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    jun_correo = forms.EmailField(max_length=254, label="Correo")
    jun_direccion = forms.CharField(label="Direccion de Casa Central", max_length=100)
    jun_mision = forms.CharField(label="Mision", max_length=300, widget=forms.Textarea(attrs={"rows": "3"}))
    jun_comuna = forms.CharField(label="Comuna", max_length=50, widget=forms.TextInput(attrs={
        "list": "opcionesComunas"}))

    class Meta:
        model = JuntaVecinos
        exclude = ('comuna_com', "jun_correo")

    def clean_jun_correo(self):
            jun_correo = self.cleaned_data.get('jun_correo')
            if JuntaVecinos.objects.filter(jun_correo=jun_correo).count() > 0:
                raise forms.ValidationError("Este correro ya se encuentra registrado")
            return jun_correo
    
    def clean_jun_telefono(self):
        jun_telefono = self.cleaned_data.get('jun_telefono')
        patron = r"^\+569\d{8}$"
        if JuntaVecinos.objects.filter(jun_telefono=jun_telefono).count() > 0:
            raise forms.ValidationError("Este telefono ya se encuentra registrado")
        else:
            if bool(re.match(patron, jun_telefono)):
                return jun_telefono
            else:
                raise forms.ValidationError("El formato del numero debe ser +56 9 1234 5678")