from django import forms
from .models import CicloLectivo, MontosCicloLectivo
from datetime import date


class CicloLectivoForm(forms.ModelForm):
    class Meta:
        model = CicloLectivo
        fields = ['anio', 'fecha_inicio', 'fecha_fin', 'habilitado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_anio(self):
        anio = self.cleaned_data['anio']
        anio_actual = date.today().year
        if anio not in [anio_actual, anio_actual + 1]:
            raise forms.ValidationError(
                f"Solo puedes habilitar el ciclo del año actual ({anio_actual}) o el siguiente ({anio_actual + 1})."
            )
        return anio

class MontosCicloLectivoForm(forms.ModelForm):
    class Meta:
        model = MontosCicloLectivo
        fields = ['ciclo_lectivo', 'nivel_educativo', 'monto_inscripcion', 'monto_cuota', 'descuento_anticipado']

from django import forms
from .models import Preinscripcion

class PreinscripcionForm(forms.ModelForm):
    class Meta:
        model = Preinscripcion
        fields = ['estudiante', 'nivel_educativo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control'}),
        }
