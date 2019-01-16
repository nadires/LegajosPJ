from django import forms
from dal import autocomplete

from .models import Empleado, ImagenEmpleado


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('imagen', 'empleado', 'seccion', )


class EmpleadoForm(forms.ModelForm):
	CHOICES = (('F', 'Femenino'), ('M', 'Masculino'))
	sexo = forms.TypedChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-control flat-blue'}), coerce=int)

	class Meta:
		model = Empleado
		fields = ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 'sexo', 'fecha_nac', 
				'estado_civil', 'nacionalidad', 'lugar_nac', 'tel_fijo', 'tel_cel', 'email', 
				'legajo')

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellido completo'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre completo'}),
			'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
			'documento' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de documento'}),
			'cuil' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Número de CUIL'}),
			'fecha_nac' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'nacionalidad' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nacionalidad', 'value': 'Argentino'}),
			'lugar_nac' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Lugar de nacimiento', 'value': 'Argentina'}),
			'tel_fijo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono fijo'}),
			'tel_cel' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono celular'}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'E-mail'}),

			'legajo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de legajo'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}