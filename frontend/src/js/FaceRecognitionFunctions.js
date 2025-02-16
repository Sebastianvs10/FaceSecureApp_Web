import * as faceMesh from '@mediapipe/face_mesh';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import { FACEMESH_TESSELATION } from "@mediapipe/face_mesh";
import axios from "axios";
import { toast} from 'react-toastify';  // Importa las funcionalidades de Toastify
import 'react-toastify/dist/ReactToastify.css'; // Asegúrate de importar los estilos de Toastify


// Variables de estado
let video = null;
let canvas = null;
let blinkCount = 0;
let requiredBlinks = 3;
let isBlinking = false;
let lastBlinkTime = 0;
let blinkCooldown = 1000;
let waitingForBlink = false;
let gazeFixed = false;
let gazeFixedDuration = 2000;
let gazeStartTime = null;
let countdownTimer = null;
let countdownValue = 3;

// Inicializa el objeto faceMesh de MediaPipe
const faceMeshInstance = new faceMesh.FaceMesh({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
});

// Configura las opciones de detección de FaceMesh
faceMeshInstance.setOptions({
  maxNumFaces: 1,
  refineLandmarks: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5,
});

faceMeshInstance.onResults(onResults);

export function initializeCamera() {
  // Asegúrate de que las variables video y canvas sean asignadas aquí
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');

  if (!video || !canvas) {
    console.error("No se encontraron los elementos de video y canvas.");
    return;
  }

  // Llamar a enableCamera para inicializar el flujo de la cámara
  enableCamera();
}
// Función que maneja los resultados de FaceMesh
function onResults(results) {
  // Asegúrate de que las variables video y canvas sean asignadas aquí
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  const canvasCtx = canvas.getContext('2d');
  canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
  canvasCtx.drawImage(results.image, 0, 0, canvas.width, canvas.height);

  if (results.multiFaceLandmarks) {
    for (const landmarks of results.multiFaceLandmarks) {
      drawConnectors(canvasCtx, landmarks, FACEMESH_TESSELATION, { color: '#C0C0C070', lineWidth: 1.5 });

      if (waitingForBlink) {
        detectBlink(landmarks); // Detecta parpadeos solo cuando se espera
      }
    }
  }
  canvasCtx.restore();
}

// Función para inicializar la cámara
export async function enableCamera() {
  if (!video || !canvas) {
    console.error("El video o el canvas no están definidos correctamente.");
    return;
  }
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    video.onloadedmetadata = () => {
      video.play();
      detectFrame(video, canvas);  // Inicia la detección una vez que el video esté listo
      startBlinkSequence();
    };
  } catch (error) {
    console.error("Error al procesar la imagen con la malla", error);
  }
}

// Función para procesar el video
async function detectFrame(video, canvas) {
  if (video.videoWidth > 0 && video.videoHeight > 0) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const imageBitmap = await createImageBitmap(video);
    await faceMeshInstance.send({ image: imageBitmap });
  }
  requestAnimationFrame(() => detectFrame(video, canvas));
}

// Función para iniciar la secuencia de parpadeos
function startBlinkSequence() {
  blinkCount = 0;
  document.getElementById('blinkMessage').textContent = `Por favor, parpadea`;
  waitingForBlink = true; // Esperar el primer parpadeo
}

// Función para detectar un parpadeo en los puntos faciales
export function detectBlink(landmarks) {

  if (!landmarks || landmarks.length < 468) {
    console.error('No se detectaron suficientes puntos faciales');
    return;
  }
  const leftEyeUpper = landmarks[159];
  const leftEyeLower = landmarks[145];
  const rightEyeUpper = landmarks[386];
  const rightEyeLower = landmarks[374];

  const leftEyeHeight = Math.abs(leftEyeUpper.y - leftEyeLower.y);
  const rightEyeHeight = Math.abs(rightEyeUpper.y - rightEyeLower.y);

  // Ajustar el umbral para la detección del parpadeo
  const blinkThreshold = 0.013; // Ajustar este valor según sea necesario

  // Si la altura de los ojos es pequeña, se detecta un parpadeo
  if (leftEyeHeight < blinkThreshold && rightEyeHeight < blinkThreshold) {
    const currentTime = Date.now();
    if (!isBlinking && currentTime - lastBlinkTime > blinkCooldown) {
      blinkCount++;
      console.log("PARPADEO", blinkCount)
      document.getElementById('blinkMessage').textContent = `¡Parpadeo ${blinkCount} detectado!`;

      lastBlinkTime = currentTime;
      isBlinking = true;
      if (blinkCount >= requiredBlinks) {
        document.getElementById('blinkMessage').textContent = `Mira fijamente a la cámara y parpadea`;
        detectGaze(landmarks); // Iniciar la detección de mirada fija
      }
    }
  } else {
    isBlinking = false;
  }
}

// Función para detectar la mirada fija
export function detectGaze(landmarks) {
  if (!landmarks || landmarks.length < 468) {
    console.error('No se detectaron suficientes puntos faciales para la mirada fija');
    return;
  }

  const leftEyeUpper = landmarks[159]; // Puntos clave del párpado superior izquierdo
  const leftEyeLower = landmarks[145]; // Puntos clave del párpado inferior izquierdo
  const rightEyeUpper = landmarks[386]; // Puntos clave del párpado superior derecho
  const rightEyeLower = landmarks[374]; // Puntos clave del párpado inferior derecho

  // Calcular la altura de los ojos (distancia entre párpado superior e inferior)
  const leftEyeHeight = Math.abs(leftEyeUpper.y - leftEyeLower.y);
  const rightEyeHeight = Math.abs(rightEyeUpper.y - rightEyeLower.y);

  // Ajustar el umbral para la detección de ojos abiertos (mirada fija)
  const openEyeThreshold = 0.001; // Ajustar este valor según sea necesario

  // Detectar si los ojos están abiertos (mirada fija)
  if (leftEyeHeight > openEyeThreshold && rightEyeHeight > openEyeThreshold) {
    // Si el usuario acaba de empezar a mirar fijamente, inicializamos el tiempo
    if (!gazeStartTime) {
      gazeStartTime = Date.now();
    }
    // Calcular cuánto tiempo ha mantenido la mirada fija
    const gazeElapsed = Date.now() - gazeStartTime;

    // Si ha mantenido la mirada fija el tiempo suficiente, iniciar cuenta regresiva
    if (gazeElapsed >= gazeFixedDuration && !gazeFixed) {
      gazeFixed = true;
      document.getElementById('blinkMessage').textContent = `Mantén la mirada fija...`;
      startCountdown();
    }
  } else {
    // Reiniciar el temporizador y el contador si el usuario no está mirando fijamente
    gazeFixed = false;
    gazeStartTime = null;
    resetCountdown();
    document.getElementById('blinkMessage').textContent = `Mira fijamente a la cámara`;
  }
}

// Función para iniciar el temporizador de cuenta regresiva
function startCountdown() {
  countdownValue = 3;
  document.getElementById('blinkMessage').textContent = `Capturando en ${countdownValue}...`;

  countdownTimer = setInterval(() => {
    countdownValue--;
    if (countdownValue > 0) {
      document.getElementById('blinkMessage').textContent = `Capturando en ${countdownValue}...`;
    } else {
      clearInterval(countdownTimer);
      document.getElementById('blinkMessage').textContent = `Capturada la imagen`;

      // Verificar la ruta actual
      const currentPath = window.location.pathname;

      // Llamar a la función correspondiente según la ruta
      if (currentPath === '/login') {
        captureImageLogin();  // Llamar a la función de login
      } else if (currentPath === '/register') {
        captureImage();  // Llamar a la función de registro
      } else {
        console.error("Ruta no válida para captura de imagen.");
      }
    }
  }, 1000);
}


// Función para reiniciar la cuenta regresiva
function resetCountdown() {
  if (countdownTimer) {
    clearInterval(countdownTimer);
    countdownTimer = null;
    document.getElementById('blinkMessage').textContent = 'Mira fijamente a la cámara';
  }
}

// Función para capturar la imagen y enviar el formulario
function captureImage() {
  const canvas = document.getElementById('canvas');
  const video = document.getElementById('video');
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataURL = canvas.toDataURL('image/png'); // Captura la imagen como una cadena base64

  // Obtener los valores del formulario
  const formData = {
    email: document.querySelector('[name="email"]').value,
    password: document.querySelector('[name="password1"]').value,
    name_user: document.querySelector('[name="name_user"]').value,
    user_code: document.querySelector('[name="user_code"]').value,
    face_data: dataURL, // Agregar la imagen en formato base64
  };
  // Enviar los datos a la API
  axios.post('http://127.0.0.1:8000/api/register/', formData)
  .then((response) => {

   // Redirigir al usuario después de 3 segundos (3000 milisegundos)
    setTimeout(() => {
      window.location.href = '/';  // Redirigir a la página de inicio
    }, 2000);  // Retraso de 2 segundos
    toast.success('¡Usuario registrado exitosamente!');
  })
  .catch((error) => {
    console.error('Error al enviar los datos:' + error.response?.data?.error);
    // Redirigir al usuario después de 3 segundos si hay un error
    setTimeout(() => {
      window.location.href = '/register';  // Redirigir a la página de inicio
    }, 5000);  // Retraso de 3 segundos
    toast.error('¡Error al registrar el usuario:' + error.response?.data?.error);
  });

}

// Función para capturar la imagen y enviar el formulario de Login
function captureImageLogin() {
  const canvas = document.getElementById('canvas');
  const video = document.getElementById('video');
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataURL = canvas.toDataURL('image/png'); // Captura la imagen como una cadena base64

  const email = document.querySelector('[name="email"]').value;

  // Verificar que el email no esté vacío
  if (!email) {
    toast.error('Por favor, ingresa tu Email');
    return;
  }

  // Crear el objeto de datos a enviar
  const formData = {
    email: email,  // Solo el nombre de usuario
    face_data: dataURL,  // Imagen en formato base64
  };

  // Enviar los datos a la API para login
  axios.post('http://127.0.0.1:8000/api/login/', formData)
    .then((response) => {

      // Guardar tokens en localStorage
      localStorage.setItem("accessToken", response.data.tokens.access);
      localStorage.setItem("refreshToken", response.data.tokens.refresh);

      // Redirigir al usuario al Home
      window.location.href = '/dashboard';  // Redirigir a la página de inicio
      toast.success('¡Bienvenido de nuevo!');
    })
    .catch((error) => {
      console.error('Error al enviar los datos:', error.response?.data || error);

      // Mostrar mensaje de error y redirigir a la página de login
      toast.error(error.response?.data.message);

      setTimeout(() => {
        window.location.href = '/login';  // Redirigir a la página de login
      }, 2000);  // Retraso de 3 segundos
    });
}



// Función para validar el nombre de usuario y proceder al siguiente tab
export const validateAndNext = async () => {
  const email = document.getElementById('email').value;
  const blinkMessageError = document.getElementById('blinkMessageError');

  if (email.trim() === '') {
    blinkMessageError.textContent = 'Por favor, diligencie el campo de usuario.';
    blinkMessageError.style.color = 'red';
    return false; // Si no está diligenciado, retornar false
  } else {
    blinkMessageError.textContent = ''; // Limpiar mensaje de error

    // Obtener el token CSRF desde el meta tag
    const csrfToken = window.csrfToken;

    try {
      // Hacer una solicitud AJAX para verificar el nombre de usuario
      const response = await fetch('http://127.0.0.1:8000/api/check-email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({ 'email': email })
      });

      const data = await response.json();

      if (data.exists) {
        return {success: true, message: ''}; // Si el usuario está registrado, retornar true
      } else {
        blinkMessageError.textContent = 'El usuario no está registrado.';
        blinkMessageError.style.color = 'red';
        return {success: false, message: 'El usuario no está registrado.'}; // Si el usuario no está registrado, retornar false
      }
    } catch (error) {
      console.error('Error al verificar el usuario:', error);

      if (error.name === 'TypeError' && error.message.includes('NetworkError')) {
        // Verifica si el error es un error de red
        blinkMessageError.textContent = 'No se puede conectar al servidor. Verifica tu conexión a internet.';
        blinkMessageError.style.color = 'red';
        return {success: false, message: 'No hay conexión con el servidor. Verifica tu red.'}; // Error de conexión
      }

      // Otro tipo de error (por ejemplo, servidor caído)
      blinkMessageError.textContent = 'Error al verificar el usuario. Intenta nuevamente más tarde.';
      blinkMessageError.style.color = 'red';
      return {success: false, message: 'Error al verificar el usuario. Intenta nuevamente más tarde.'}; // Error genérico
    }
  }
};




