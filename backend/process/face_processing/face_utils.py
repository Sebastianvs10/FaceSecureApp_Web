import os

import numpy as np
import cv2
import datetime
from typing import List, Tuple, Any

from django.utils import timezone
from pydantic import ValidationError
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.hashers import make_password
from ..face_processing.face_detect_models.face_detect import FaceDetectMediapipe
from ..face_processing.face_mesh_models.face_mesh import FaceMeshMediapipe
from ..face_processing.face_matcher_models.face_matcher import FaceMatcherModels
from accounts.models import CustomUser,AccessLog


class FaceUtils:
    def __init__(self):
        # face detect
        self.face_detector = FaceDetectMediapipe()
        # face mesh
        self.mesh_detector = FaceMeshMediapipe()
        # face matcher
        self.face_matcher = FaceMatcherModels()

        # variables
        self.angle = None
        self.face_db = []
        self.face_names = []
        self.distance: float = 0.0
        self.matching: bool = False
        self.distance2: float = 0.0
        self.matching2: bool = False
        self.user_registered = False
        # Cargar la clave secreta Fernet desde settings.py
        self.secret_key = settings.FERNET_SECRET_KEY.encode()  # Asegúrate de que sea bytes
        self.cipher = Fernet(self.secret_key)
    # detect
    def check_face(self, face_image: np.ndarray) -> Tuple[bool, Any, np.ndarray]:
        face_save = face_image.copy()
        check_face, face_info = self.face_detector.face_detect_mediapipe(face_image)
        return check_face, face_info, face_save

    def extract_face_bbox(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        bbox = self.face_detector.extract_face_bbox_mediapipe(w_img, h_img, face_info)
        return bbox

    def extract_face_points(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        face_points = self.face_detector.extract_face_points_mediapipe(h_img, w_img, face_info)
        return face_points

    # face mesh
    def face_mesh(self, face_image: np.ndarray) -> Tuple[bool, Any]:
        check_face_mesh, face_mesh_info = self.mesh_detector.face_mesh_mediapipe(face_image)
        return check_face_mesh, face_mesh_info

    def extract_face_mesh(self, face_image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        face_mesh_points_list = self.mesh_detector.extract_face_mesh_points(face_image, face_mesh_info, viz=True)
        return face_mesh_points_list

    def check_face_center(self, face_points: List[List[int]]) -> bool:
        check_face_center = self.mesh_detector.check_face_center(face_points)
        return check_face_center

    # crop
    def face_crop(self, face_image: np.ndarray, face_bbox: List[int]) -> np.ndarray:
        h, w, _ = face_image.shape
        offset_x, offset_y = int(w * 0.025), int(h * 0.025)
        xi, yi, xf, yf = face_bbox
        xi, yi, xf, yf = xi - offset_x, yi - (offset_y*4), xf + offset_x, yf
        return face_image[yi:yf, xi:xf]

    # save
    def save_face_data(self, face_crop: np.ndarray, user_code: str, username: str, name_user: str, password: str,
                       email: str) -> tuple:
        if face_crop is not None and face_crop.size > 0:
            # Convertir la imagen a formato binario
            _, buffer = cv2.imencode('.png', face_crop)  # Cambia el formato según necesites
            img_data = buffer.tobytes()

            # Guardar en la base de datos
            try:
                # Encriptar la imagen
                encrypted_image_data = self.cipher.encrypt(img_data)
                # Encriptar la contraseña usando Django
                encrypted_password = make_password(password)

                # Crear un nuevo usuario
                user = CustomUser(
                    username=username,
                    email=email,
                    user_code=user_code,
                    name_user=name_user,
                    face_data=encrypted_image_data,
                    password=encrypted_password
                )
                user.full_clean()  # Verifica que los datos sean válidos antes de guardar
                user.save()

                # Si todo va bien, se retorna True con un mensaje de éxito
                return True, "Usuario registrado exitosamente."

            except ValidationError as e:
                # Retorna False con el mensaje de error de validación
                return False, f"Error de validación: {str(e)}"
            except Exception as e:
                # Retorna False con el mensaje de error general
                return False, f"Error al guardar la imagen: {str(e)}"
        else:
            # Retorna False con el mensaje indicando que la imagen no es válida
            return False, "La imagen está vacía o no es válida."

    # draw
    def show_state_signup(self, face_image: np.ndarray, state: bool):
        if state:
            text = 'Saving face, wait three seconds please'
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1]-baseline), (370 + dim[0], 650 + baseline), (0, 0, 0), cv2.FILLED)
            cv2.putText(face_image, text, (370, 650-5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 1)
            self.mesh_detector.config_color((0, 255, 0))

        else:
            text = 'Face processing, see the camera please!'
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 0), 1)
            self.mesh_detector.config_color((255, 0, 0))

    def show_state_login(self, face_image: np.ndarray, state: bool):
        if state:
            text = 'Approved face, come in please!'
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 1)
            self.mesh_detector.config_color((0, 255, 0))

        elif state is None:
            text = 'Comparing faces, see the camera and wait 3 seconds please!'
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (250, 650 - dim[1] - baseline), (250 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (250, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 0), 1)
            self.mesh_detector.config_color((255, 255, 0))

        elif state is False:
            text = 'Face no approved, please register!'
            size_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            dim, baseline = size_text[0], size_text[1]
            cv2.rectangle(face_image, (370, 650 - dim[1] - baseline), (370 + dim[0], 650 + baseline), (0, 0, 0),
                          cv2.FILLED)
            cv2.putText(face_image, text, (370, 650 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 0), 1)
            self.mesh_detector.config_color((255, 0, 0))

    def read_face_database(self) -> Tuple[List[np.ndarray], List[str], List[str]]:
        self.face_db: List[np.ndarray] = []
        self.face_names: List[str] = []
        self.names_user: List[str] = []
        self.face_codes: List[str] = []  # Lista para almacenar códigos

        # Leer todos los usuarios desde la base de datos
        users = CustomUser.objects.all().only('face_data', 'username', 'user_code', 'name_user')
        for user in users:
            # Convertir la imagen binaria a un formato que OpenCV pueda leer
            face_image = np.frombuffer(user.face_data, np.uint8)
            img_read = cv2.imdecode(face_image, cv2.IMREAD_COLOR)  # Decodificar imagen
            if img_read is not None:
                self.face_db.append(img_read)
                self.face_names.append(user.username)  # Almacenar el nombre del usuario
                self.face_codes.append(user.user_code)  # Almacenar el código del usuario
                self.names_user.append(user.name_user)  # Almacenar el código del usuario
        print(f'Base de datos de caras cargada con {len(self.face_db)} imágenes.')
        return self.face_db, self.face_names, self.names_user, self.face_codes, f'Comparing {len(self.face_db)} faces!'

    def face_matching(self, current_face: np.ndarray, stored_face: np.ndarray, username: str) -> Tuple[
        bool, str, float]:
        try:
            # Verificamos si las caras son válidas (no son None ni vacías)
            if current_face is None or stored_face is None:
                raise ValueError("Una de las caras es None, no se puede proceder con la comparación.")

            # Redimensionar las imágenes para que tengan el mismo tamaño
            current_face = cv2.resize(current_face, (stored_face.shape[1], stored_face.shape[0]))

            # Convertir a formato adecuado (de RGB a BGR)
            current_face = cv2.cvtColor(current_face, cv2.COLOR_RGB2BGR)
            stored_face = cv2.cvtColor(stored_face, cv2.COLOR_RGB2BGR)

            # Realiza la comparación directa entre la cara actual y la almacenada
            matching, distance = self.face_matcher.face_matching_facenet_model(current_face, stored_face)

            # Si la comparación es positiva, retornamos la coincidencia
            if matching:
                return True, username, distance
            else:
                # Si no hay coincidencia, retornamos False
                return False, '', 0.0

        except Exception as e:
            # Si ocurre cualquier error, lo capturamos y retornamos False, sin nombre de usuario
            print(f"Error en face_matching: {e}")
            return False, '', 0.0

    def face_matching2(self, current_face: np.ndarray, face_db: List[np.ndarray], name_db: List[str]) -> Tuple[bool, str]:
        username: str = ''
        current_face = cv2.cvtColor(current_face, cv2.COLOR_RGB2BGR)
        for idx, face_img in enumerate(face_db):
            self.matching, self.distance = self.face_matcher.face_matching_facenet_model(current_face, face_img)

            if self.matching:
                username = name_db[idx]
                return self.matching, username
        return False, 'Face unknown'

    def check_in_user(self, email: str, distance: float):
        if email is None:
            return False, 'Error: email no proporcionado.'

        if distance is None:
            return False, 'Error: distancia no proporcionada.'

        # Buscar al usuario por el email (USERNAME_FIELD es email en CustomUser)
        user = CustomUser.objects.filter(username=email).first()

        if user:  # Verifica si el usuario existe
            now = timezone.now()  # Obtener la hora actual
            success = True  # Asumimos que el acceso es exitoso

            try:
                # Registrar el acceso en la base de datos
                AccessLog.objects.create(
                    user=user,
                    success=success,
                    timestamp=now,
                    ip_address='192.168.1.1',  # Obtener IP real si se pasa en la petición
                    distance=distance  # Asegúrate de que distance sea un número flotante
                )
                return True, f'Acceso concedido: {email}'
            except Exception as e:
                return False, f"Error al registrar acceso: {e}"
        else:
            return False, 'Acceso denegado: usuario no encontrado.'

    def load_user_face_image(self, username):
        # Cargar la imagen almacenada desde la base de datos
        user = CustomUser.objects.get(username=username)
        if user and user.face_data:  # Asegúrate de que haya datos en face_data
            # Convertir los datos de la imagen a bytes si es un memoryview
            face_data_bytes = user.face_data.tobytes() if isinstance(user.face_data, memoryview) else user.face_data

            # Desencriptar los datos de la imagen usando la clave secreta
            cipher = Fernet(settings.FERNET_SECRET_KEY.encode())  # Asegúrate de que sea bytes
            decrypted_image_data = cipher.decrypt(face_data_bytes)

            # Convertir los datos binarios desencriptados a una imagen en formato adecuado
            nparr = np.frombuffer(decrypted_image_data, np.uint8)
            stored_face = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if stored_face is not None:
                return stored_face
            else:
                print("Error al procesar la imagen de la cara almacenada.")
                return None
        else:
            print("No hay datos de cara disponibles para este usuario.")
            return None


    def decrypt_image(self, encrypted_data: bytes) -> bytes:
        """Método para desencriptar los datos de imagen."""
        return self.cipher.decrypt(encrypted_data)
