from django.contrib import admin
from lists.models import Genre, Movie
from django.contrib.auth.admin import UserAdmin

from .forms import MoovieUserCreationForm, MoovieUserChangeForm
from .models import MoovieUser


class MoovieUserAdmin(UserAdmin):
    add_form = MoovieUserCreationForm
    form = MoovieUserChangeForm
    model = MoovieUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MoovieUser, MoovieUserAdmin)
# Register your models here.
