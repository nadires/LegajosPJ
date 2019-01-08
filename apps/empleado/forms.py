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
			'apellido' : forms.TextInput(attrs={'class':'clase'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
			'cuil' : forms.NumberInput(attrs={'class':'form-control'}),
			'dni' : forms.NumberInput(attrs={'class':'form-control'}),
			'legajo' : forms.NumberInput(attrs={'class':'form-control'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}