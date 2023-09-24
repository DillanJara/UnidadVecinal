from django import forms

from .models import *

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
    class Meta:
        model = JuntaVecinos
        fields = '__all__'  # O puedes especificar los campos que quieras incluir

    # Puedes personalizar los campos del formulario si es necesario
    jun_nombre = forms.CharField(label="Nombre de la Junta de Vecinos", max_length=50)
    jun_fecha_fundacion = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    jun_nombre_villa = forms.CharField(label="Nombre de la Unidad Territorial", max_length=50)
    jun_telefono = forms.CharField(label="Telefono", max_length=12)
    jun_correo = forms.EmailField(max_length=254)
    jun_direccion = forms.CharField(label="Direccion de Casa Central", max_length=100)
    jun_mision = forms.CharField(label="Mision", max_length=300, widget=forms.Textarea())
    comuna_com_id = forms.ModelChoiceField(queryset=Comuna.objects.all(), label="Comuna")