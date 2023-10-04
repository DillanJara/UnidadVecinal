from django import forms
from ..models import *
from datetime import date
import re

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
    mie_password         = forms.CharField(max_length=150, min_length=8, label="Contraseña", widget=forms.PasswordInput())
    mie_password_2       = forms.CharField(max_length=150, label="Confirmar Contraseña", widget=forms.PasswordInput())

    class Meta:
        model   = Miembro
        fields = ["mie_rut", "mie_dv", "mie_nombre", "mie_ap_paterno", "mie_ap_materno",]
        """exclude = ("mie_estado", "junta_vecinos_jun", "cargo_car", "mie_dv", "mie_fecha_nacimiento",
            "mie_telefono", "mie_correo", )"""

    def clean_mie_rut(self):
        mie_rut = self.cleaned_data.get("mie_rut")
        if Miembro.objects.filter(mie_rut=mie_rut).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_rut=mie_rut).count() > 0:
            raise forms.ValidationError("Esta persona ya se encuentra registrada")
        return mie_rut

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
        if edad < 18:
            raise forms.ValidationError("Debes ser mayor de 18 años para registrarte.")
        else :
            return mie_fecha_nacimiento

    def clean_mie_telefono(self):
        mie_telefono = self.cleaned_data.get('mie_telefono')
        patron = r"^\+569\d{8}$"
        if Miembro.objects.filter(mie_telefono=mie_telefono).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_telefono=mie_telefono).count():
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

class AgregarMiembro(forms.ModelForm):
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
    mie_password         = forms.CharField(max_length=150, min_length=8, label="Contraseña", widget=forms.PasswordInput())
    mie_password_2       = forms.CharField(max_length=150, label="Confirmar Contraseña", widget=forms.PasswordInput())
    mie_junta_vecinos    = forms.CharField(label="Junta de Vecinos", max_length=50, widget=forms.TextInput(attrs={
        "list": "opcionesJuntasVecinos"}))

    class Meta:
        model   = Miembro
        fields = ["mie_rut", "mie_dv", "mie_nombre", "mie_ap_paterno", "mie_ap_materno",]

    def clean_mie_rut(self):
        mie_rut = self.cleaned_data.get("mie_rut")
        if Miembro.objects.filter(mie_rut=mie_rut).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_rut=mie_rut).count() > 0:
            raise forms.ValidationError("Esta persona ya se encuentra registrada")
        return mie_rut

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
        if edad < 18:
            raise forms.ValidationError("Debes ser mayor de 18 años para registrarte.")
        else :
            return mie_fecha_nacimiento

    def clean_mie_telefono(self):
        mie_telefono = self.cleaned_data.get('mie_telefono')
        patron = r"^\+569\d{8}$"
        if Miembro.objects.filter(mie_telefono=mie_telefono).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_telefono=mie_telefono).count():
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

    def clean_mie_junta_vecinos(self):
        mie_junta_vecinos = self.cleaned_data.get('mie_junta_vecinos')
        if JuntaVecinos.objects.filter(jun_nombre=mie_junta_vecinos).count() > 0:
            return mie_junta_vecinos
        else:
            raise forms.ValidationError("La junta de vecinos ingresada no existe. Ingrese una valida")
