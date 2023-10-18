from django import forms
from django.utils import timezone
from datetime import datetime, time, timedelta
from ..models import *

class AgregarReserva(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ["miembro_mie", "espacio_esp", "res_hora_fin"]

    res_fecha       = forms.DateField(label="Fecha Reserva", widget=forms.TextInput(attrs={
        "type": "date"
    }))
    horas_disponibles = [
        ["18:00", "18:00" ],
        ["19:00", "19:00" ],
        ["20:00", "20:00" ],
        ["21:00", "21:00" ],
        ["22:00", "22:00" ],
    ]
    res_hora_inicio = forms.CharField(label="Hora inicio", widget=forms.Select(choices=horas_disponibles))

    def clean_res_fecha(self):
        res_fecha = self.cleaned_data.get("res_fecha")
        fecha_actual = timezone.now().date()
        if res_fecha < fecha_actual:
            raise forms.ValidationError('La fecha seleccionada no es valida')
        else:
            return res_fecha

    def clean_res_hora_inicio(self):
        hora_actual = datetime.now().time()
        res_hora_inicio = time.fromisoformat(self.cleaned_data.get("res_hora_inicio"))
        # hora_fin = (datetime.combine(datetime.min, res_hora_inicio) + timedelta(hours=1)).time()
        if res_hora_inicio < hora_actual:
            raise forms.ValidationError('La hora seleccionada no es valida')
        else:
            return res_hora_inicio