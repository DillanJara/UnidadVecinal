from django import forms
from ..models import Actividad, TipoActividad

class AgregarActividad(forms.ModelForm):
    class Meta:
        model = Actividad
        exclude = ["act_id", "act_imagen", "junta_vecinos_jun"]

    tipo_actividad_tip_act = forms.ModelChoiceField(label="Tipo de Actividad", queryset=TipoActividad.objects.all())
    act_fecha              = forms.DateField(label="Fecha de Evento", widget=forms.TextInput(attrs={"type": "date"}))
    act_descripcion        = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={"rows": "3"}))
    act_cupo               = forms.IntegerField(label="Cupo", help_text="Disponibilidad para la Actividad", min_value=0, max_value=200)
    act_cuota              = forms.IntegerField(label="Cuota (Opcional)", required=False, min_value=0)