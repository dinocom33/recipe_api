from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from core.models import Tag, Ingredient

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'is_staff', 'is_superuser', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    list_filter = ['email', 'name', 'is_active', 'is_staff', 'is_superuser', 'last_login']
    search_fields = ['email', 'name']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(models.User, UserAdmin)


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'time_minutes', 'price', 'link']
    list_filter = ['title']
    search_fields = ['title', 'description', 'link']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user__email']
    search_fields = ['name', 'user__email']


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user__email']
    search_fields = ['name', 'user__email']
