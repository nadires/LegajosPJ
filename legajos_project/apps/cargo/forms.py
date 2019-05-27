
from django import forms

from .models import Cargo
import datetime


class CargoForm(forms.ModelForm):
    fecha_fin_cargo_anterior = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
               'data-mask': ''}))

    class Meta:
        model = Cargo
        exclude = ['actual']

        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'agrupamiento': forms.Select(attrs={'class': 'form-control'}),
            'situacion': forms.Select(attrs={'class': 'form-control'}),
            'jurisdiccion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso_cargo': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),
            'fecha_vencimiento_cargo': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),
            'instrumento_legal': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 4400', 'autocomplete': 'off'}),
            'tipo_instrumento_legal': forms.Select(attrs={'class': 'form-control'}),
            'fecha_instr_legal': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),

            # 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
        }

    def clean_fecha_fin_cargo_anterior(self):
        # Valida que la fecha de fin de cargo anterior sea menor a la de ingreso al nuevo cargo
        fecha_fin_cargo_anterior = self.cleaned_data.get("fecha_fin_cargo_anterior")
        fecha_ingreso_cargo = self.cleaned_data.get("fecha_ingreso_cargo")
        if fecha_fin_cargo_anterior:
            if fecha_ingreso_cargo and fecha_fin_cargo_anterior >= fecha_ingreso_cargo:
                raise forms.ValidationError(
                    "La fecha de fin del cargo anterior debe ser menor que la fecha de ingreso al nuevo cargo")
        else:
            fecha_fin_cargo_anterior = fecha_ingreso_cargo + datetime.timedelta(days=-1)
        return fecha_fin_cargo_anterior
