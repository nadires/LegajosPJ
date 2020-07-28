
from django import forms
from dal import autocomplete

from .models import DependenciaLaboral
import datetime


class DependenciaLaboralForm(forms.ModelForm):
    empleado = forms.UUIDField(required=False)

    class Meta:
        model = DependenciaLaboral
        exclude = ['actual']

        widgets = {
            'circunscripcion': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'organismo': forms.Select(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso_dependencia': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),
            'instrumento_legal': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 4400', 'autocomplete': 'off'}),
            'tipo_instrumento_legal': forms.Select(attrs={'class': 'form-control'}),
            'fecha_instr_legal': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),

        }
