from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .views import *

# from .models import Perfil

# class RegistroForm(UserCreationForm):
#     first_name = forms.CharField(max_length=140, required=True)
#     last_name = forms.CharField(max_length=140, required=False)
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         proxy = True
#         model = User
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'password1',
#             'password2',
#         ]
# class PerfilForm (ModelForm):
#     class Meta:
#         model=Perfil