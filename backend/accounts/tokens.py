# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

from rest_framework_simplejwt.tokens import RefreshToken

class AccessToken:
    @staticmethod
    def for_user(user):
        """Genera un token de acceso para un usuario"""
        refresh = RefreshToken.for_user(user)
        return refresh
