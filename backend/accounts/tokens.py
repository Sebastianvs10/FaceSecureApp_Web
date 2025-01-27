from rest_framework_simplejwt.tokens import RefreshToken

class AccessToken:
    @staticmethod
    def for_user(user):
        """Genera un token de acceso para un usuario"""
        refresh = RefreshToken.for_user(user)
        return refresh
