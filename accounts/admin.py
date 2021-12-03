from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'is_staff', 'is_active','is_superuser')
    list_filter = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'password')}),
        ('Permissions', {'fields': ['is_staff', 'is_active','is_superuser']})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_staff')}
        ),
    )
    ordering = ['email']
    search_fields = ['email']
