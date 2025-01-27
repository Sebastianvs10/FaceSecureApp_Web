import face_recognition as fr
from deepface import DeepFace
from typing import Tuple
import cv2
import numpy as np
from django.conf import settings

class FaceMatcherModels:
    def __init__(self):
        self.models = [
            "VGG-Face",
            "Facenet",
            "Facenet512",
            "OpenFace",
            "DeepFace",
            "DeepID",
            "ArcFace",
            "Dlib",
            "SFace",
            "GhostFaceNet",
        ]

    def face_matching_face_recognition_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        face_1 = cv2.cvtColor(face_1, cv2.COLOR_BGR2RGB)
        face_2 = cv2.cvtColor(face_2, cv2.COLOR_BGR2RGB)

        face_loc_1 = [(0, face_1.shape[0], face_1.shape[1], 0)]
        face_loc_2 = [(0, face_2.shape[0], face_2.shape[1], 0)]

        face_1_encoding = fr.face_encodings(face_1, known_face_locations=face_loc_1)[0]
        face_2_encoding = fr.face_encodings(face_2, known_face_locations=face_loc_2)

        matching = fr.compare_faces(face_1_encoding, face_2_encoding, tolerance=0.55)
        distance = fr.face_distance(face_1_encoding, face_2_encoding)

        return matching[0], distance[0]

    def face_matching_vgg_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[0])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_facenet_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            # Verificar que las imágenes no estén vacías o sean nulas
            if face_1 is None or face_2 is None:
                raise ValueError("Las imágenes proporcionadas son nulas o vacías.")
            # Mostrar las formas de las imágenes para depurar
            print(f"Forma de face_1: {face_1.shape}, Forma de face_2: {face_2.shape}")
            # Detectar el nivel de luminosidad de la imagen
            if self.is_dark_image(face_1):
                face_1 = self.enhance_image(face_1)  # Mejorar la imagen solo si es oscura

            if self.is_dark_image(face_2):
                face_2 = self.enhance_image(face_2)  # Mejorar la imagen solo si es oscura

            # Asegurarse de que las caras estén en formato RGB (DeepFace trabaja con RGB)
            if face_1.shape[2] == 3 and face_2.shape[2] == 3:  # Verificar que las imágenes tengan 3 canales (RGB)
                face_1 = cv2.cvtColor(face_1, cv2.COLOR_BGR2RGB)
                face_2 = cv2.cvtColor(face_2, cv2.COLOR_BGR2RGB)
            else:
                raise ValueError("Las imágenes deben tener 3 canales (RGB)")

            # Verificar si los tamaños de las caras son compatibles
            if face_1.shape != face_2.shape:
                print(f"Redimensionando imagen 2 de {face_2.shape} a {face_1.shape}")
                # Redimensionar la imagen de la cara 2 para que coincida con la cara 1
                face_2 = cv2.resize(face_2, (face_1.shape[1], face_1.shape[0]))

            # Usar DeepFace para verificar la similitud entre las dos caras
            result = DeepFace.verify(face_1, face_2, model_name=self.models[1])

            print("RESULTADO:", result)

            # Revisar si la verificación fue exitosa
            if 'verified' in result:
                matching = result['verified']
                distance = result['distance']
                print(f"Coincidencia: {matching}, Distancia: {distance}")

                # Ajustar el umbral: si la distancia es mayor que un umbral específico, consideramos que no hay coincidencia
                umbral_similitud = settings.UMBRAL_SIMILITUD # Puedes ajustar este umbral a tu necesidad
                if distance < umbral_similitud:
                    return True, distance  # Coincidencia
                else:
                    return False, distance  # No coincidencia debido a la alta distancia

            else:
                print("Error: No se pudo obtener la coincidencia de las caras.")
                return False, 0.0

        except ValueError as ve:
            print(f"Error de valor: {ve}")
            return False, 0.0
        except cv2.error as ce:
            print(f"Error en OpenCV: {ce}")
            return False, 0.0
        except Exception as e:
            print(f"Error en face_matching_facenet_model: {e}")
            return False, 0.0

    def face_matching_facenet512_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[2])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_openface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[3])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_deepface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[4])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_deepid_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[5])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_arcface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[6])
            print("RESULTADO:", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_dlib_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[7])
            print("RESULTADO:", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_sface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[8])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def face_matching_ghostfacenet_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.models[9])
            print("RESULTADO", result)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0

    def is_dark_image(self, image: np.ndarray) -> bool:
        """
        Determina si una imagen está demasiado oscura.
        Compara el valor promedio de los píxeles en escala de grises con un umbral.
        Si el valor promedio es menor que el umbral, la imagen se considera oscura.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
        mean_brightness = np.mean(gray_image)  # Calcular la media de brillo de la imagen

        print(f"Brillo promedio: {mean_brightness}")  # Mostrar el valor del brillo promedio

        # Umbral de luminosidad para considerar la imagen oscura
        brightness_threshold = 100  # Este umbral puedes ajustarlo según el caso
        return mean_brightness < brightness_threshold

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Mejora la imagen para condiciones de poca iluminación aplicando varias técnicas:
        - Ecualización del histograma
        - Aumento de contraste y brillo.
        """
        # Convertir a escala de grises
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Ecualización del histograma para mejorar el contraste
        equalized_image = cv2.equalizeHist(gray_image)

        # Convertir de nuevo a color (RGB) para que sea compatible con DeepFace
        enhanced_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)

        # Opcional: Aumento de brillo y contraste
        enhanced_image = self.adjust_brightness_contrast(enhanced_image, alpha=1.5, beta=50)

        return enhanced_image

    def adjust_brightness_contrast(self, image: np.ndarray, alpha: float, beta: int) -> np.ndarray:
        """
        Ajusta el brillo y contraste de la imagen.
        - alpha: controla el contraste (1.0 = sin cambio, >1.0 aumenta el contraste).
        - beta: controla el brillo (0 = sin cambio).
        """
        # Ajustar brillo y contraste
        adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted_image