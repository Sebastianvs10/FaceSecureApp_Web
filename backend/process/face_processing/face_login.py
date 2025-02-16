import numpy as np
import resend
from rest_framework import request

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
                print(info_check.email)
                name_user = info_check.name_user
                # Calcular el porcentaje de similitud
                similarity_percentage = (1 - distance) * 100

                # Verificar si la similitud es mayor que el umbral (0.4)
                if distance <= 0.4:
                    similarity_message = f"La similitud entre tu rostro y el rostro registrado es del {similarity_percentage:.2f}%."
                else:
                    similarity_message = f"La similitud entre tu rostro y el rostro registrado es baja ({similarity_percentage:.2f}%). Por favor, asegúrate de que tu rostro sea claramente visible."

                # Crear los parámetros del correo
                params = {
                    "from": "FaceSecure <onboarding@facesecure.online>",
                    "to": [email],  # Usamos el correo del usuario registrado
                    "subject": "Inicio de sesión exitoso",  # Asunto actualizado
                    "html": f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f4f4f4;
                                    padding: 20px;
                                }}
                                .container {{
                                    width: 100%;
                                    max-width: 600px;
                                    margin: 0 auto;
                                    background-color: #ffffff;
                                    padding: 20px;
                                    border-radius: 8px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                h1 {{
                                    color: #333333;
                                    text-align: center;
                                }}
                                p {{
                                    font-size: 16px;
                                    color: #555555;
                                }}
                                .user-info {{
                                    background-color: #f9f9f9;
                                    padding: 15px;
                                    border-radius: 5px;
                                    margin-top: 20px;
                                }}
                                .user-info p {{
                                    margin: 5px 0;
                                }}
                                .logo {{
                                    text-align: center;
                                    margin-bottom: 20px;
                                }}
                                .logo img {{
                                    width: 150px;
                                    height: auto;
                                }}
                                .footer {{
                                    text-align: center;
                                    font-size: 14px;
                                    color: #888888;
                                    margin-top: 20px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="logo">
                                    <!-- Aquí pones la URL del logo que quieras mostrar -->
                                    <img src="https://cdn-icons-png.flaticon.com/512/5972/5972778.png" alt="Logo de FaceSecure">
                                </div>
                                <h1>¡Bienvenido, {name_user}!</h1>
                                <p>Tu inicio de sesión fue exitoso en nuestro sistema FaceSecure.</p>



                                <p>{similarity_message}</p>

                                <div class="footer">
                                    <p>Si tienes alguna duda, no dudes en contactarnos.</p>
                                    <p>&copy; 2025 FaceSecure. Todos los derechos reservados.</p>
                                </div>
                            </div>
                        </body>
                    </html>
                    """
                }

                # Configura la clave API de Resend
                resend.api_key = "re_UMJQeZGM_Kq1WvnBDoEYHqTx7GjTpbZsc"

                try:
                    # Enviar el correo
                    email_response = resend.Emails.send(params)
                    print(email_response)
                except Exception as e:
                    print(f"Error al enviar el correo: {str(e)}")

                return face_crop, True, {'Email': email,'distance': distance}
        return face_crop, False, 'Usuario no aprobado'


