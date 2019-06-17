from django.db import models
"""from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Python 3
def __str__(self): 
        return self.usuario.username

@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()
"""

# class Perfil(models.Model):
#     user = models.ForeignKey(User, unique=True)
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     location = models.CharField(max_length=140)
#     gender = models.CharField(max_length=140)
#     profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
#     def __unicode__(self): return u'Profile of user: %s' % self.user.username