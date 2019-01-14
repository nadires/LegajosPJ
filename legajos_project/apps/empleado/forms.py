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
		fields = ('apellido', 'nombre', 'cuil', 'dni', 'legajo')

		labels = {
			'apellido' : 'Apellido: ',
			'nombre' : 'Nombre: ',
			'cuil' : 'CUIL: ',
			'dni' : 'DNI N°: ',
			'legajo' : 'Legajo N°: ',
		}

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellido completo'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre completo'}),
			'cuil' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de CUIL'}),
			'dni' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de documento'}),
			'legajo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de legajo'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}