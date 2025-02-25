# Importa las bibliotecas necesarias para el reconocimiento facial
import base64

import cv2
import numpy as np
from accounts.models import CustomUser, AccessLog
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse
from process.face_processing.face_login import FaceLogIn
from process.face_processing.face_signup import FaceSignUp
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .tokens import AccessToken


class UserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Obtener los datos de la solicitud
        image_data = request.data.get('face_data')  # Asegúrate de que 'face_data' sea el campo enviado
        email = request.data.get('email')
        name_user = request.data.get('name_user')
        password = request.data.get('password')  # Suponiendo que usas 'password' para la contraseña
        user_code = request.data.get('user_code')

        if not image_data or not email or not user_code or not name_user or not password:
            return Response({'error': 'Faltan datos requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar la imagen (base64 a imagen)
        try:
            if ';base64,' in image_data:
                format, imgstr = image_data.split(';base64,')
                img_data = base64.b64decode(imgstr)
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Realiza cualquier preprocesamiento con la imagen (por ejemplo, FaceSignUp)
                face_sign_up = FaceSignUp()
                processed_img, save_image, info = face_sign_up.process(img, user_code, name_user, password, email)

                if not save_image:
                    return Response({'error': info}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Formato de imagen incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'Error procesando la imagen: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Primero, obtenemos los datos de la solicitud
        email = request.data.get('email')
        image_data = request.data.get('face_data')

        # Verificamos que ambos campos existan
        if not email or not image_data:
            return Response({"detail": "Email and image data are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Decodificar la imagen capturada
        format, imgstr = image_data.split(';base64,')
        img_data = base64.b64decode(imgstr)
        nparr = np.frombuffer(img_data, np.uint8)
        face_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Procesar la imagen para comparar
        face_login = FaceLogIn()
        processed_img, user_access, user_info = face_login.process(face_image, email)

        if user_access:
            # Si el acceso es válido, obtenemos el usuario desde la base de datos
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Ahora, validamos los datos del serializador sin necesidad de la contraseña
            serializer = CustomUserSerializer(user)
            # Generamos el token de acceso
            token = AccessToken.for_user(user)

            # Preparamos los datos de respuesta
            data = serializer.data
            data["tokens"] = {
                "refresh": str(token),
                "access": str(token.access_token)
            }

            # También guardamos información adicional en la sesión si es necesario
            request.session['user_code'] = user.user_code
            request.session['username'] = user.email
            request.session['name_user'] = user.name_user
            request.session['distance'] = user_info.get('distance', None)  # Si se utiliza
            request.session['role'] = user.role
            request.session['token'] = str(token)

            return Response(data, status=status.HTTP_200_OK)
        else:
            # Si la comparación de la imagen no es válida, respondemos con un error
            return Response({'status': 'error', 'message': 'Acceso denegado, no se encontraron coincidencias'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"detail": "An error occurred while logging out."}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user

@api_view(['POST'])
def check_email(request):
    serializer = EmailValidationSerializer(data=request.data)
    if serializer.is_valid():
        # Si el usuario existe, devolver respuesta positiva
        return JsonResponse({'exists': True})
    else:
        # Si el usuario no existe, devolver respuesta negativa
        return JsonResponse({'exists': False, 'error': 'Usuario no encontrado'}, status=400)

# Vista para obtener todos los usuarios
class AdminUsersView(APIView):
    permission_classes = [IsAuthenticated]  # Asegúrate de que el usuario está autenticado

    def get(self, request):
        # Obtener todos los usuarios, ordenados por 'date_joined' (de los más recientes a los más antiguos)
        users = CustomUser.objects.all().order_by('-date_joined')

        # Aplicar la paginación
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)

        # Serializar los usuarios
        serializer = CustomUserSerializer(result_page, many=True)

        # Retornar los datos en formato JSON con paginación
        return paginator.get_paginated_response(serializer.data)


def get_user_info(request, user_id):
    try:
        # Obtener el usuario de la base de datos
        user = CustomUser.objects.get(id=user_id)

        # Convertir los datos de la imagen a bytes si es un memoryview
        face_data_bytes = user.face_data.tobytes() if isinstance(user.face_data, memoryview) else user.face_data

        # Desencriptar los datos de la imagen usando la clave secreta
        cipher = Fernet(settings.FERNET_SECRET_KEY.encode())  # Asegúrate de que sea bytes
        decrypted_image_data = cipher.decrypt(face_data_bytes)

        # Convertir los datos binarios desencriptados a una imagen en formato adecuado
        nparr = np.frombuffer(decrypted_image_data, np.uint8)
        face_crop = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Verificar si la imagen se procesó correctamente
        if face_crop is None:
            return JsonResponse({'error': 'Error al procesar la imagen'}, status=500)

        # Convertir la imagen a base64 para visualizarla en HTML
        _, buffer = cv2.imencode('.png', face_crop)  # Se usa '.png', puedes cambiar el formato si lo necesitas
        face_data_base64 = base64.b64encode(buffer).decode('utf-8') if buffer is not None else None

        # Obtener la trazabilidad de acceso
        access_logs = AccessLog.objects.filter(user=user).values('timestamp', 'success', 'distance').order_by('-timestamp')
        access_logs_list = list(access_logs)

        user_info = {
            'id': user.id,
            'username': user.email,
            'user_code': user.user_code,
            'name_user': user.name_user,
            'role': user.role,
            'email': user.email,
            'password': user.password,
            'face_data': f"data:image/png;base64,{face_data_base64}" if face_data_base64 else None,
            'access_logs': access_logs_list  # Agregar la trazabilidad
        }
        return JsonResponse(user_info)
    except CustomUser.DoesNotExist:
        return JsonResponse({'Error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'Error': f'Error inesperado: {str(e)}'}, status=500)

# Clase de paginación
class CustomPagination(PageNumberPagination):
    page_size = 10  # Número de elementos por página
    page_size_query_param = 'limit'  # Permite personalizar el tamaño de la página desde el cliente
    max_page_size = 100  # Limitar el tamaño máximo de la página