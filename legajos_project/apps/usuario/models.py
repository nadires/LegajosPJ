from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('El campo Email es obligatorio')
        if not password:
            raise ValueError('El campo Password es obligatorio')
        user_obj = self.model(
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.superuser = True
        user.save(using=self._db)
        return user


class ActivosManager(models.Manager):
    def get_queryset(self, queryset=None):
        qs = super().get_queryset()
        return qs.filter(active=True, superuser=False)


class TipoUsuario(models.Model):
    tipo = models.TextField('Tipo de Usuario')

    def __str__(self):
        return self.tipo


def default_tipo_usuario():
    tipo_usuario = TipoUsuario.objects.get(tipo='Anonimo')
    if not tipo_usuario:
        tipo_usuario.tipo = 'Anonimo'
        tipo_usuario.save()
    return tipo_usuario


class Usuario(AbstractBaseUser):
    SEXO = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(_('date joined'), default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    superuser = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.SET(default_tipo_usuario), related_name='usuarios_tipo', null=True)
    foto = models.ImageField(upload_to='usuarios', blank=True, null=True)

    objects = UserManager()
    activos = ActivosManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['contrasenia']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def front_perm(self):
        return self.admin or self.tipo == 'PR'

    @property
    def politico_perm(self):
        return self.admin or self.tipo == 'PO'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def get_nombre_completo(self):
        return '{}, {}'.format(self.apellido, self.nombre)

    @property
    def get_name(self):
        return '%s' % (self.email)

    def __str__(self):
        return '%s' % (self.get_name)
