
from django import forms
from dal import autocomplete

from .models import Empleado, Cargo, ImagenEmpleado, DependenciaLaboral, Circunscripcion
import datetime


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('imagen', 'empleado', 'seccion',)


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 'sexo', 'estado_civil',
                  'nacionalidad', 'fecha_nac', 'lugar_nac', 'tel_fijo', 'tel_cel', 'email',
                  'domicilio', 'barrio', 'piso', 'dpto', 'localidad', 'cod_postal', 'departamento', 'provincia',
                  'legajo', 'fecha_ingreso', 'horario')

        widgets = {
            'apellido': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Apellido completo', 'autocomplete': 'off'}),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre completo', 'autocomplete': 'off'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'cuil': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Formato 00-00000000-0', 'autocomplete': 'off',
                       'data-inputmask': "'mask': '99-99999999-9'", 'data-mask': ''}),
            'sexo': forms.RadioSelect(attrs={'class': 'form-control flat-blue'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nacionalidad', 'value': 'Argentino',
                       'autocomplete': 'off'}),
            'fecha_nac': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),
            'lugar_nac': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Lugar de nacimiento', 'value': 'Argentina',
                       'autocomplete': 'off'}),
            'tel_fijo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono fijo'}),
            'tel_cel': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono celular'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'autocomplete': 'off'}),
            'domicilio': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Domicilio', 'autocomplete': 'off'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barrio', 'autocomplete': 'off'}),
            'piso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Piso', 'autocomplete': 'off'}),
            'dpto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Dpto', 'autocomplete': 'off'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            'cod_postal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),

            'legajo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de legajo'}),
            'fecha_ingreso': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'data-inputmask': "'alias': 'dd/mm/yyyy'",
                       'data-mask': ''}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            # 'familiares': autocomplete.ModelSelect2Multiple(url='familiar-autocomplete', attrs={'class':'form-control', 'data-html': True})
        }

    def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        cuil = cuil.replace(" ", "")
        cuil = cuil.replace(".", "")
        cuil = cuil.replace("_", "")
        try:
            a, b, c = cuil.split('-')  # Separo el cuil en 3 variables, la b es el dni
        except ValueError:
            raise forms.ValidationError('El CUIL debe tener el formato 00-00000000-0')

        if len(a) != 2:
            raise forms.ValidationError('El CUIL debe tener el formato 00-00000000-0 con 2 dígitos iniciales')
        if len(b) != 8:
            raise forms.ValidationError('El CUIL debe tener el formato 00-00000000-0 con 8 dígitos centrales')
        if len(c) != 1:
            raise forms.ValidationError('El CUIL debe tener el formato 00-00000000-0 con 1 dígito central')
        nro_dni = str(int(b)).strip()  # Limpio los espacios en blanco del dni
        documento = str(self.cleaned_data['documento']).strip()
        if documento != nro_dni:
            raise forms.ValidationError('N° de documento y CUIL no coinciden')

        base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]  # Se usa para validación del cuil

        nro_cuil = cuil.replace("-", "")  # remuevo las barras
        nro_cuil = nro_cuil.replace(" ", "")
        nro_cuil = nro_cuil.replace(".", "")

        if len(nro_cuil) != 11:
            raise forms.ValidationError('El CUIL debe tener el formato 00-00000000-0')

        aux = 0
        for i in range(len(nro_cuil) - 1):
            aux += int(nro_cuil[i]) * base[i]

        aux = 11 - (aux - (int(aux / 11) * 11))

        if aux == 11:
            aux = 0
        if aux == 10:
            aux = 9

        if aux != int(nro_cuil[len(nro_cuil) - 1]):
            raise forms.ValidationError('El N° de CUIL no es válido')

        return cuil

    # def clean(self):
    #     cleaned_data = super(EmpleadoForm, self).clean()
    #     fecha_ingreso = cleaned_data['fecha_ingreso']
    #     fecha_nac = cleaned_data['fecha_nac']
    #     if fecha_ingreso < fecha_nac:
    #         raise forms.ValidationError('Fecha de ingreso incorrecta, no puede ser menor a la fecha de nacimiento')
    #     return cleaned_data

    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data['fecha_nac']
        if fecha_nac > datetime.date.today():
            raise forms.ValidationError('Fecha de nacimiento incorrecta')
        return fecha_nac

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data['fecha_ingreso']
        if 'fecha_nac' in self.cleaned_data:
            if fecha_ingreso < self.cleaned_data['fecha_nac']:
                raise forms.ValidationError('Fecha de ingreso incorrecta, no puede ser menor a la fecha de nacimiento')
        return fecha_ingreso


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


class DependenciaLaboralForm(forms.ModelForm):
    # dependencias_list = forms.TypedChoiceField(required=False, widget=autocomplete.ModelSelect2(url='dependencias-autocomplete-list'))
    dependencias_list = forms.ModelChoiceField(required=False, queryset=Circunscripcion.objects.values_list('circunscripcion'), widget=autocomplete.ModelSelect2(url='dependencias-autocomplete', attrs={'class': 'form-control', 'data-html': True}))

    class Meta:
        model = DependenciaLaboral
        exclude = ['actual']

        widgets = {
            'circunscripcion': autocomplete.ModelSelect2(url='dependencias-autocomplete', attrs={'class': 'form-control', 'data-html': True}),
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


# class ListadoDependenciasForm(forms.Form):
#     dependencias_list = forms.CharField(required=False,
#                                         widget=autocomplete.Select2(
#                                             url='dependencias-autocomplete',
#                                             attrs={'class': 'form-control', 'data-html': True})
#                                         )
