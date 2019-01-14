from django import forms
from dal import autocomplete

from .models import Empleado, ImagenEmpleado


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('imagen', 'empleado', 'seccion', )


class EmpleadoForm(forms.ModelForm):
	class Meta:
		model = Empleado
		fields = ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 'sexo', 'legajo')

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellido completo'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre completo'}),
			'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
			'documento' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de documento'}),
			'cuil' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Número de CUIL', 'data-inputmask': "'mask': ['999-999-9999 [x99999]', '+099 99 99 9999[9]-9999']", 'data-mask': ''}),
			'sexo': forms.RadioSelect(attrs={'class': 'form-control flat-blue'}),

			'legajo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de legajo'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}