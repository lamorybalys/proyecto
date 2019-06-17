from django.contrib import admin
from .models import  User
# Register your models here.

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User,Notificacion


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('cedula','email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_archivista','is_analista_jubilacion','is_analista_social','is_analista_vacaciones','is_trabajador',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('cedula','email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','cedula','email', 'password1', 'password2')}
        ),
    )
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('cedula','email', 'first_name','is_superuser','is_archivista','is_analista_jubilacion','is_analista_social','is_analista_vacaciones','is_trabajador')
    list_filter = ('is_staff', 'is_superuser','is_archivista', 'is_active','is_analista_jubilacion','is_analista_social','is_analista_vacaciones','is_trabajador', 'groups')
    search_fields = ('first_name', 'last_name', 'cedula','email')
    ordering = ('cedula','email',)
    readonly_fields = ('last_login', 'date_joined',)

admin.site.register(User,UserAdmin)
class AdminNoti(admin.ModelAdmin):
	list_display = ["usuario","url","tipo","estatus"]

admin.site.register(Notificacion, AdminNoti)