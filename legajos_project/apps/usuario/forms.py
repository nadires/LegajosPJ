from dal import autocomplete
from django import forms
from django.contrib.auth import authenticate
from django.utils.text import capfirst
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UserModel
# users/forms.py
from .models import Usuario


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated contrasenia."""
    contrasenia1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    contrasenia2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # admin = forms.BooleanField(label='Asignar como Administrador',
    #                            widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
    #                            required=False)

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'apellido', 'sexo', 'tipo', 'foto', 'admin', 'superuser')

        widgets = {
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'admin': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
        }

    def clean_contrasenia2(self):
        # Check that the two contrasenia entries match
        contrasenia1 = self.cleaned_data.get("contrasenia1")
        contrasenia2 = self.cleaned_data.get("contrasenia2")
        if contrasenia1 and contrasenia2 and contrasenia1 != contrasenia2:
            raise forms.ValidationError("Las contraseñas no son iguales")
        return contrasenia2

    def save(self, commit=True):
        # Save the provided contrasenia in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["contrasenia1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("No es posible ver la contraseña, puede cambiarla directamente "
                                                    "usando <a href=\"password/\">este formulario</a>."))

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'nombre', 'apellido', 'sexo', 'tipo', 'foto', 'admin', 'superuser')

        widgets = {
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Save the provided contrasenia in hashed format
        user = super(UserAdminChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["contrasenia"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autofocus': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    error_messages = {
        'invalid_login': (
            "Por favor ingrese un Email y Contraseña correctos. Tenga en cuenta que ambos "
            "campos son sensibles a mayúsculas"
        ),
        'inactive': ("Esta cuenta está inactiva."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        self.fields['email'].max_length = self.username_field.max_length or 254
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )
