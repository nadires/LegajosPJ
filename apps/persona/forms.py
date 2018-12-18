from django import forms
from dal import autocomplete

from .models import Persona, Seccion, Imagen


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ('imagen', 'persona', 'seccion', )


class PersonaForm(forms.ModelForm):
	class Meta:
		model = Persona
		fields = ('apellido', 'nombre', 'cuil', 'dni', 'legajo', 'familiares')

		labels = {
			'apellido' : 'Apellido: ',
			'nombre' : 'Nombre: ',
			'cuil' : 'CUIL: ',
			'dni' : 'DNI N°: ',
			'legajo' : 'Legajo N°: ',
			'familiares' : 'Familiares: ',
		}

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'clase'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
			'cuil' : forms.NumberInput(attrs={'class':'form-control'}),
			'dni' : forms.NumberInput(attrs={'class':'form-control'}),
			'legajo' : forms.NumberInput(attrs={'class':'form-control'}),
			'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control'})
		}