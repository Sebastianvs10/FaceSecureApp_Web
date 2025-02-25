import face_recognition as fr
import cv2
import os
import numpy as np
import dlib
from deepface import DeepFace
from typing import Tuple
from imutils import face_utils
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

    def detect_glasses(self, face_image: np.ndarray) -> bool:
        # Utiliza el clasificador de OpenCV para detectar gafas
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

        glasses = glasses_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(glasses) > 0:
            return True  # Gafas detectadas
        return False  # No se detectaron gafas

    def remove_glasses_area(self, face_image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

        glasses = glasses_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in glasses:
            # Puedes optar por borrar el área o difuminarla
            face_image[y:y + h, x:x + w] = 0  # Borrar la zona de los ojos (puedes aplicar otro método como difuminar)

        return face_image

    def face_matching_facenet_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            if face_1 is None or face_2 is None:
                raise ValueError("Las imágenes proporcionadas son nulas o vacías.")

            # Preprocesamiento y alineación
            face_1 = self.preprocess_image(face_1)
            face_2 = self.preprocess_image(face_2)

            face_1 = self.align_face(face_1)
            face_2 = self.align_face(face_2)

            # Ajuste por gafas o gorras
            umbral_similitud = settings.UMBRAL_SIMILITUD
            if self.detect_glasses(face_1) or self.detect_glasses(face_2):

                umbral_similitud += 0.1  # Tolerancia extra

            # Asegurarse de que estén en RGB
            face_1 = cv2.cvtColor(face_1, cv2.COLOR_BGR2RGB)
            face_2 = cv2.cvtColor(face_2, cv2.COLOR_BGR2RGB)

            # Redimensionar si es necesario
            if face_1.shape != face_2.shape:
                face_2 = cv2.resize(face_2, (face_1.shape[1], face_1.shape[0]))

            # Verificación con DeepFace
            result = DeepFace.verify(face_1, face_2, model_name=self.models[1])
            print("RESULTADO", result)
            matching = result['verified']
            distance = result['distance']
            if distance < umbral_similitud:
                return matching, distance
            return False, distance

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

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # Convertir a escala de grises para ecualización
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # Aplicar suavizado para reducir reflejos o ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Reconstruir imagen en RGB
        image = cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB)
        return image

    def align_face(self, image: np.ndarray) -> np.ndarray:
        # Ruta al archivo del predictor (ajusta según tu sistema)
        predictor_path = os.path.join(os.getcwd(), "shape_predictor_68_face_landmarks.dat")

        # Inicializar detector y predictor
        detector = dlib.get_frontal_face_detector()
        try:
            predictor = dlib.shape_predictor(predictor_path)
        except RuntimeError as e:
            print(f"Error al cargar el predictor: {e}. Verifica la ruta: {predictor_path}")
            return image  # Si falla, devuelve la imagen sin alinear

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)

        if len(rects) == 0:
            print(" No se detectaron rostros para alinear.")
            return image

        # Tomar el primer rostro detectado
        rect = rects[0]
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extraer coordenadas de los ojos (índices típicos para 68 landmarks: 36-41 para ojo izquierdo, 42-47 para ojo derecho)
        left_eye = shape[36:42].mean(axis=0)  # Centro del ojo izquierdo
        right_eye = shape[42:48].mean(axis=0)  # Centro del ojo derecho

        # Calcular el ángulo de rotación entre los ojos
        dY = right_eye[1] - left_eye[1]
        dX = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dY, dX))  # Ángulo en grados

        # Calcular el centro de los ojos (punto de rotación)
        eyes_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)

        # Tamaño deseado entre los ojos (puedes ajustar este valor)
        desired_eye_distance = 0.35  # Proporción del ancho de la imagen
        current_eye_distance = np.sqrt(dX ** 2 + dY ** 2)
        scale = (desired_eye_distance * image.shape[1]) / current_eye_distance

        # Obtener la matriz de transformación (rotación + escala)
        M = cv2.getRotationMatrix2D(eyes_center, angle, scale)

        # Ajustar la traslación para centrar la imagen
        M[0, 2] += (image.shape[1] * 0.5 - eyes_center[0])
        M[1, 2] += (image.shape[0] * 0.25 - eyes_center[1])  # Ajustar verticalmente

        # Aplicar la transformación
        aligned_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC)

        return aligned_image