from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "user_code", "name_user", "role", "face_data")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    face_data = serializers.FileField(required=False, allow_null=True)  # Usamos FileField para manejar archivos binarios

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "user_code", "name_user", "password1", "password2", "role", "face_data")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        # Validación de contraseñas
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden!")

        password = attrs.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError("La contraseña debe contener al menos 8 caracteres!")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        # Crear el usuario
        user = CustomUser.objects.create_user(password=password, **validated_data)

        # Si se incluye face_data, se guarda
        if 'face_data' in validated_data:
            user.face_data = validated_data['face_data']
            user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales Incorrectas!")

class UsernameValidationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            return value
        raise serializers.ValidationError('El usuario no está registrado.')