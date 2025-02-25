# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomAdminUser(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        
        model = CustomUser