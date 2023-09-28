from django import forms
from .models import *
from datetime import date
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
def validar_rut(rut_numero, rut_verificador):
    digito_verificador = '0' if rut_verificador.lower() == 'k' else rut_verificador
    # Calcular el dígito verificador esperado
    suma = 0
    multiplicador = 2
    for digito in reversed(rut_numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    digito_esperado = 11 - resto if resto > 1 else 0

    # Comparar el dígito verificador calculado con el proporcionado
    if str(digito_esperado) == digito_verificador:
        return True
    else:
        return False


class AgregarJuntaVecinos(forms.ModelForm):
    jun_nombre          = forms.CharField(label="Nombre de la Junta de Vecinos", max_length=50)
    jun_fecha_fundacion = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), label="Fecha de fundacion")
    jun_nombre_villa    = forms.CharField(label="Nombre de la Unidad Territorial", max_length=50)
    jun_telefono        = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    jun_correo          = forms.EmailField(max_length=254, label="Correo")
    jun_direccion       = forms.CharField(label="Direccion de Casa Central", max_length=100)
    jun_mision          = forms.CharField(label="Mision", max_length=300, widget=forms.Textarea(attrs={"rows": "3"}))
    jun_comuna          = forms.CharField(label="Comuna", max_length=50, widget=forms.TextInput(attrs={
        "list": "opcionesComunas"}))

    class Meta:
        model   = JuntaVecinos
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
    
    def clean_jun_comuna(self):
        jun_comuna = self.cleaned_data.get('jun_comuna')
        if Comuna.objects.filter(com_nombre=jun_comuna).count() > 0:
            return jun_comuna
        else:
            raise forms.ValidationError("Ingrese una comuna existente")
        

class AgregarPresidente(forms.ModelForm):
    mie_rut              = forms.IntegerField(label="Rut", max_value=99999999, min_value=1)
    mie_dv               = forms.CharField(max_length=1, label="DV")
    mie_nombre           = forms.CharField(max_length=30, label="Nombre")
    mie_ap_paterno       = forms.CharField(max_length=30, label="Apellido Paterno")
    mie_ap_materno       = forms.CharField(max_length=30, label="Apellido Materno")
    mie_telefono         = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    mie_direccion        = forms.CharField(max_length=30, label="Direccion")
    mie_correo           = forms.EmailField(max_length=245, label="Correo")
    mie_fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento", widget=forms.TextInput(attrs={
        "type": "date"
    }))
    mie_password         = forms.CharField(max_length=100, label="Contraseña", widget=forms.PasswordInput())
    mie_password_2       = forms.CharField(max_length=100, label="Confirmar Contraseña", widget=forms.PasswordInput())

    class Meta:
        model   = Miembro
        fields = ["mie_rut", "mie_dv", "mie_nombre", "mie_ap_paterno", "mie_ap_materno",]
        """exclude = ("mie_estado", "junta_vecinos_jun", "cargo_car", "mie_dv", "mie_fecha_nacimiento", 
            "mie_telefono", "mie_correo", )"""

    def clean_mie_dv(self):
        mie_rut = self.cleaned_data.get('mie_rut')
        mie_dv = self.cleaned_data.get('mie_dv')
        regex_dv = r'^[0-9kK]$'
        if re.match(regex_dv, mie_dv):
            if validar_rut(str(mie_rut), mie_dv):
                return mie_dv
            else:
                raise forms.ValidationError("Ingrese un digito verificador valido")
        else:
            raise forms.ValidationError("Ingrese un digito verificador valido")
        

    def clean_mie_fecha_nacimiento(self):
        mie_fecha_nacimiento = self.cleaned_data.get('mie_fecha_nacimiento')
        fecha_actual = date.today()

        edad = fecha_actual.year - mie_fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (mie_fecha_nacimiento.month, mie_fecha_nacimiento.day))

        # Realiza la validación
        if edad < 18:
            raise forms.ValidationError("Debes ser mayor de 18 años para registrarte.")
        else :
            return mie_fecha_nacimiento

    def clean_mie_telefono(self):
        mie_telefono = self.cleaned_data.get('mie_telefono')
        patron = r"^\+569\d{8}$"
        if Miembro.objects.filter(mie_telefono=mie_telefono).count() > 0:
            raise forms.ValidationError("Este telefono ya se encuentra registrado")
        else:
            if bool(re.match(patron, mie_telefono)):
                return mie_telefono
            else:
                raise forms.ValidationError("El formato del numero debe ser +56 9 1234 5678")

    def clean_mie_correo(self):
        mie_correo = self.cleaned_data.get('mie_correo')
        if Miembro.objects.filter(mie_correo=mie_correo).count() > 0:
            raise forms.ValidationError("Este correo ya se encuentra registrado")
        return mie_correo

    def clean_mie_password_2(self):
        mie_password = self.cleaned_data.get('mie_password')
        mie_password_2 = self.cleaned_data.get('mie_password_2')

        if mie_password == mie_password_2:
            return mie_password_2
        else:
            raise forms.ValidationError("Las contraseñas no coinciden")
