from django import forms
from ..models import *
import re

class AgregarFamiliarMiembro(forms.ModelForm):
    fam_mie_rut        = forms.IntegerField(label="Rut", max_value=99999999, min_value=1,)
    fam_mie_dv         = forms.CharField(max_length=1, label="DV")
    fam_mie_nombre     = forms.CharField(max_length=30, label="Nombre")
    fam_mie_ap_paterno = forms.CharField(max_length=30, label="Apellido Paterno")
    fam_mie_ap_materno = forms.CharField(max_length=30, label="Apellido Materno")
    fam_mie_telefono   = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    lista_parentesco = [
        ["Abuelo/a", "Abuelo/a"],
        ["Padre", "Padre"],
        ["Madre", "Madre"],
        ["Hermano/a", "Hermano/a"],
        ["Pareja/Conviviente", "Pareja/Conviviente"],
        ["Hijo/a", "Hijo/a"],
        ["Nieto", "Nieto"],
        ["Otro", "Otro"]
    ]
    fam_mie_parentesco = forms.CharField(label="Parentesco", widget=forms.Select(choices=lista_parentesco))

    class Meta:
        model   = FamiliarMiembro
        exclude = ["miembro_mie", ]

    def clean_fam_mie_rut(self):
        mie_rut = self.cleaned_data.get("fam_mie_rut")
        if Miembro.objects.filter(mie_rut=mie_rut).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_rut=mie_rut).count() > 0:
            raise forms.ValidationError("Esta persona ya se encuentra registrada")
        return mie_rut

    def clean_fam_mie_dv(self):
        fam_mie_rut = self.clean_fam_mie_rut()
        fam_mie_dv = self.cleaned_data.get('fam_mie_dv')
        regex_dv = r'^[0-9kK]$'
        if re.match(regex_dv, fam_mie_dv):
            return fam_mie_dv
        else:
            raise forms.ValidationError("Ingrese un digito verificador valido")

    def clean_fam_mie_telefono(self):
        fam_mie_telefono = self.cleaned_data.get('fam_mie_telefono')
        patron = r"^\+569\d{8}$"
        if Miembro.objects.filter(mie_telefono=fam_mie_telefono).count() > 0 or FamiliarMiembro.objects.filter(fam_mie_telefono=fam_mie_telefono).count():
            raise forms.ValidationError("Este telefono ya se encuentra registrado")
        else:
            if bool(re.match(patron, fam_mie_telefono)):
                return fam_mie_telefono
            else:
                raise forms.ValidationError("El formato del numero debe ser +56 9 1234 5678")


class editarFamiliarMiembro(forms.ModelForm):
    class Meta:
        model   = FamiliarMiembro
        exclude = ["miembro_mie", "fam_mie_parentesco"]

    lista_parentesco = [
        ["Abuelo/a", "Abuelo/a"],
        ["Padre", "Padre"],
        ["Madre", "Madre"],
        ["Hermano/a", "Hermano/a"],
        ["Pareja/Conviviente", "Pareja/Conviviente"],
        ["Hijo/a", "Hijo/a"],
        ["Nieto", "Nieto"],
        ["Otro", "Otro"]
    ]
    fam_mie_rut        = forms.IntegerField(label="Rut", max_value=99999999, min_value=1, disabled=True)
    fam_mie_dv         = forms.CharField(max_length=1, label="DV", disabled=True)
    fam_mie_nombre     = forms.CharField(max_length=30, label="Nombre")
    fam_mie_ap_paterno = forms.CharField(max_length=30, label="Apellido Paterno")
    fam_mie_ap_materno = forms.CharField(max_length=30, label="Apellido Materno")
    fam_mie_telefono   = forms.RegexField(regex=r'^\+569\d{8}$', max_length=12, label="Telefono", error_messages={
            "formato": "El formato del numero debe ser +56912345678"
        })
    fam_mie_parentesco = forms.CharField(label="Parentesco", widget=forms.Select(choices=lista_parentesco))