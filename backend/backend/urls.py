# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("accounts.urls"))
]
