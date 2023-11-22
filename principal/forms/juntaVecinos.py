from django import forms
from ..models import JuntaVecinos, Comuna
from django.utils import timezone
import re

class AgregarJuntaVecinos(forms.ModelForm):
    jun_rol_municipal   = forms.IntegerField(label="Rol Municipal", min_value=1, max_value=5000)
    jun_nombre          = forms.CharField(label="Nombre de la Junta de Vecinos", max_length=50)
    jun_fecha_fundacion = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), label="Fecha de fundacion", help_text="Personalidad Juridica")
    jun_nombre_villa    = forms.CharField(label="Nombre de la Unidad Territorial", max_length=50)
    jun_telefono        = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono de Contacto", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    jun_correo          = forms.EmailField(max_length=254, label="Correo Institucional")
    jun_direccion       = forms.CharField(label="Direccion de Casa Central", max_length=100)
    jun_mision          = forms.CharField(label="Mision", required=False, max_length=300, widget=forms.Textarea(attrs={"rows": "3"}))
    jun_comuna          = forms.CharField(label="Comuna", max_length=50, widget=forms.TextInput(attrs={
        "list": "opcionesComunas"}))

    class Meta:
        model   = JuntaVecinos
        exclude = ("comuna_com", "jun_habilitada", "jun_directiva", "jun_certificado_vigencia")

    def clean_jun_fecha_fundacion(self):
        jun_fecha_fundacion = self.cleaned_data.get("jun_fecha_fundacion")
        fecha_actual = timezone.now().date()
        if jun_fecha_fundacion > fecha_actual:
            raise forms.ValidationError('La fecha seleccionada no es valida')
        else:
            return jun_fecha_fundacion

    def clean_jun_correo(self):
        jun_correo = self.cleaned_data.get('jun_correo')
        if JuntaVecinos.objects.filter(jun_correo=jun_correo).count() > 0:
            raise forms.ValidationError("Este correo ya se encuentra registrado")
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

    def clean_jun_comuna(self):
        jun_comuna = self.cleaned_data.get('jun_comuna')
        if Comuna.objects.filter(com_nombre=jun_comuna).count() > 0:
            return jun_comuna
        else:
            raise forms.ValidationError("Ingrese una comuna existente")