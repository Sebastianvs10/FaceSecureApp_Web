# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

import numpy as np

from ..face_processing.face_utils import FaceUtils


class FaceLogIn:
    def __init__(self):
        self.face_utilities = FaceUtils()
        self.matcher = None
        self.comparison = False
        self.cont_frame = 0

    def process(self, face_image: np.ndarray, email: str = None):
        # Cargar la imagen del usuario almacenada
        stored_face = self.face_utilities.load_user_face_image(email)
        if stored_face is None:
            return None, False, {'distance': 0.0}

        # Paso 1: Verificar detección de la cara
        check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
        if not check_face_detect:
            return face_image, False, '¡No se detectó la cara!'

        # Paso 2: Malla facial
        check_face_mesh, face_mesh_info = self.face_utilities.face_mesh(face_image)
        if not check_face_mesh:
            return face_image, False, '¡No se detectó la malla facial!'

        # Paso 3: Extraer la malla facial
        face_mesh_points_list = self.face_utilities.extract_face_mesh(face_image, face_mesh_info)

        # Paso 4: Verificar el centro de la cara
        if not self.face_utilities.check_face_center(face_mesh_points_list):
            return face_image, False, 'Cara no centrada'

        # Mostrar estado de inicio de sesión
        self.face_utilities.show_state_login(face_image, state=self.matcher)

        # Paso 5: Extraer información de la cara
        face_bbox = self.face_utilities.extract_face_bbox(face_image, face_info)
        face_crop = self.face_utilities.face_crop(face_save, face_bbox)

        # Comparar con la imagen almacenada
        if stored_face is not None:
            # Se realiza la comparación de la cara actual con la almacenada
            self.matcher, email, distance = self.face_utilities.face_matching(face_crop, stored_face, email)

            if self.matcher:
                check_user_in, info_check = self.face_utilities.check_in_user(email, distance)
                return face_crop, True, {'Email': email,'distance': distance}
        return face_crop, False, 'Usuario no aprobado'


