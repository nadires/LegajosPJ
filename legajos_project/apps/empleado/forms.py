from django import forms
from dal import autocomplete

from .models import Empleado, Cargo, ImagenEmpleado
from datetime import datetime, timedelta 


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('imagen', 'empleado', 'seccion', )


class EmpleadoForm(forms.ModelForm):

	class Meta:
		model = Empleado
		fields = ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 'sexo', 'estado_civil', 
				'nacionalidad', 'fecha_nac', 'lugar_nac', 'tel_fijo', 'tel_cel', 'email', 
				'domicilio', 'barrio', 'piso', 'dpto', 'localidad', 'cod_postal', 'departamento', 'provincia',
				'legajo', 'fecha_ingreso', 'horario')

		widgets = {
			'apellido' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellido completo', 'autocomplete':'off'}),
			'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre completo', 'autocomplete':'off'}),
			'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
			'documento' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de documento'}),
			'cuil' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Número de CUIL', 'autocomplete':'off'}),
			'sexo': forms.RadioSelect(attrs={'class': 'form-control flat-blue'}),
			'estado_civil': forms.Select(attrs={'class': 'form-control'}),
			'nacionalidad' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nacionalidad', 'value': 'Argentino', 'autocomplete':'off'}),
			'fecha_nac' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'lugar_nac' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Lugar de nacimiento', 'value': 'Argentina', 'autocomplete':'off'}),
			'tel_fijo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono fijo'}),
			'tel_cel' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Teléfono celular'}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'E-mail', 'autocomplete':'off'}),
			'domicilio' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Domicilio', 'autocomplete':'off'}),
			'barrio' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Barrio', 'autocomplete':'off'}),
			'piso' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Piso', 'autocomplete':'off'}),
			'dpto' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'N° Dpto', 'autocomplete':'off'}),
			'localidad' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Localidad'}),
			'cod_postal' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Código Postal'}),
			'departamento': forms.Select(attrs={'class': 'form-control'}),
			'provincia': forms.Select(attrs={'class': 'form-control'}),

			'legajo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de legajo'}),
			'fecha_ingreso' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'horario': forms.Select(attrs={'class': 'form-control'}),
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}


class CargoForm(forms.ModelForm):
	fecha_fin_cargo_anterior = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}))

	class Meta:
		model = Cargo
		exclude = ['actual']

		widgets = {
			'cargo' : forms.Select(attrs={'class': 'form-control'}),
			'nivel' : forms.Select(attrs={'class': 'form-control'}),
			'agrupamiento': forms.Select(attrs={'class': 'form-control'}),
			'situacion' : forms.Select(attrs={'class': 'form-control'}),
			'jurisdiccion' : forms.Select(attrs={'class': 'form-control'}),
			'fecha_ingreso_cargo': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'fecha_vencimiento_cargo' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			'instrumento_legal' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 4400', 'autocomplete':'off'}),
			'tipo_instrumento_legal' : forms.Select(attrs={'class': 'form-control'}),
			'fecha_instr_legal' : forms.DateInput(attrs={'class':'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'", 'data-mask': ''}),
			
			# 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
		}

	def clean_fecha_fin_cargo_anterior(self):
		# Valida que la fecha de fin de cargo anterior sea menor a la de ingreso al nuevo cargo
		fecha_fin_cargo_anterior = self.cleaned_data.get("fecha_fin_cargo_anterior")
		fecha_ingreso_cargo = self.cleaned_data.get("fecha_ingreso_cargo")
		if fecha_fin_cargo_anterior:
			if fecha_ingreso_cargo and fecha_fin_cargo_anterior >= fecha_ingreso_cargo:
				raise forms.ValidationError("La fecha de fin del cargo anterior debe ser menor que la fecha de ingreso al nuevo cargo")
		else:
			fecha_fin_cargo_anterior = fecha_ingreso_cargo + timedelta(days=-1)
		return fecha_fin_cargo_anterior