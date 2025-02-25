# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
            model = CustomUser
            fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
        class Meta:
            model = CustomUser
            fields = ("email",)

