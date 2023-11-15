from django import forms
from ..models import *

class AgregarNoticia(forms.ModelForm):
    class Meta:
        model = Noticia
        exclude = ["not_id", "not_fecha", "not_imagen", "miembro_mie", ]

    not_titulo      = forms.CharField(label="Titulo de la noticia", max_length=50)
    not_subtitulo   = forms.CharField(label="Subtitulo de la noticia", max_length=100, widget=forms.Textarea(
        {"rows": "2"}
    ))
    not_descripcion = forms.CharField(label="Descripcion", max_length=300, widget=forms.Textarea(
        {"rows": "4"}
    ))