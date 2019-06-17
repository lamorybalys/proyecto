from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, cedula, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not cedula:
            raise ValueError('No introdujo una cedula')
        #email = self.normalize_email(email)
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(cedula, password, **extra_fields)

    def create_superuser(self, cedula, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(cedula, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), max_length=30, unique=True,blank=True)
    cedula = models.CharField(_('Cedula'), max_length=30,unique=True)
    first_name = models.CharField(_('Nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('Apellido'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Activo'), default=True)
    is_superuser = models.BooleanField(_('Administrador'), default=False)
    is_archivista = models.BooleanField(_('Arc'), default=False)
    
    is_analista_jubilacion = models.BooleanField(_('Jub'), default=False)
    is_analista_social = models.BooleanField(_('Seg'), default=False)

    is_analista_vacaciones = models.BooleanField(_('Vac'), default=False)
    is_trabajador = models.BooleanField(_('Trab'), default=False)


    is_staff = models.BooleanField(_('Staff'), default=True)



    objects = UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

class Notificacion(models.Model):
	usuario= models.ForeignKey(User,null=True,blank=True)
	contenido = models.CharField(max_length=800)
	tip = (
		("trabajador","trabajador"),
		("vacaciones","vacaciones"),
		("jubilacion","jubilacion"),
		("seguro","seguro"),
	)
	url = models.CharField(max_length=200)
	tipo = models.CharField(max_length=100, choices=tip)
	estatus = models.BooleanField(default=False)
	fecha = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '{},{}'.format(str(self.usuario),self.estatus)