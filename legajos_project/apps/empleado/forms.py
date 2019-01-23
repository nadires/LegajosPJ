from django import forms
from dal import autocomplete

from .models import Empleado, ImagenEmpleado


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('imagen', 'empleado', 'seccion', )


class EmpleadoForm(forms.ModelForm):
	CHOICES = (('Femenino', 'Femenino'), ('Masculino', 'Masculino'))


	class Meta:
		model = Empleado
		fields = ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 'sexo', 'estado_civil', 
				'nacionalidad', 'fecha_nac', 'lugar_nac', 'tel_fijo', 'tel_cel', 'email', 
				'domicilio', 'barrio', 'piso', 'dpto', 'localidad', 'cod_postal', 'departamento', 'provincia',
				'legajo', 'fecha_ingreso', 'horario')

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellido completo'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre completo'}),
			'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
			'documento' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de documento'}),
			'cuil' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Número de CUIL'}),
			'sexo': forms.RadioSelect(attrs={'class': 'form-control flat-blue'}),
			'estado_civil': forms.Select(attrs={'class': 'form-control'}),
			'nacionalidad' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nacionalidad', 'value': 'Argentino'}),
			'fecha_nac' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'lugar_nac' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Lugar de nacimiento', 'value': 'Argentina'}),
			'tel_fijo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono fijo'}),
			'tel_cel' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono celular'}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'E-mail'}),
			'domicilio' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Domicilio'}),
			'barrio' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Barrio'}),
			'piso' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Piso'}),
			'dpto' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'N° Dpto'}),
			'localidad' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Localidad'}),
			'cod_postal' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Código Postal'}),
			'departamento': forms.Select(attrs={'class': 'form-control'}),
			'provincia': forms.Select(attrs={'class': 'form-control'}),

			'legajo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de legajo'}),
			'fecha_ingreso' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'horario': forms.Select(attrs={'class': 'form-control'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}