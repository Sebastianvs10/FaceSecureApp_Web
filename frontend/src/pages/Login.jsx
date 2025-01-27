import React, { useState, useEffect } from "react";
import axios from "axios";
import '../index.css'; // Asegúrate de que el archivo CSS esté bien vinculado
import { initializeCamera, validateAndNext } from "../js/FaceRecognitionFunctions.js";
import { toast} from 'react-toastify';  // Importa las funcionalidades de Toastify
import 'react-toastify/dist/ReactToastify.css'; // Asegúrate de importar los estilos de Toastify

export default function Login() {
  const [formData, setFormData] = useState({
    username: '',
  });
  const [activeTab, setActiveTab] = useState(1);
  const [blinkMessage, setBlinkMessage] = useState('');

  // Cambiar a la siguiente pestaña y ejecutar la validación
  const nextTab = async () => {
    const isValid = await validateAndNext(); // Llamar a la función de validación y esperar el resultado
    console.log(isValid);

    if (isValid) { // Solo cambiar a la siguiente pestaña si la validación es exitosa
      setActiveTab(2); // Cambiar a la segunda pestaña
      initializeCamera(); // Inicializar la cámara
    } else {
      toast.error('Validación fallida.', error);
    }
  };


  const previousTab = () => {
    setActiveTab(1); // Volver a la primera pestaña
  };

  // Manejar el cambio en el input del formulario
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Enviar el formulario (Login)
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", formData);
      console.log("Success!", response.data);
      localStorage.setItem("accessToken", response.data.tokens.access);
      localStorage.setItem("refreshToken", response.data.tokens.refresh);
    } catch (error) {
      console.log("Error during Login!", error.response?.data);
      if (error.response && error.response.data) {
        Object.keys(error.response.data).forEach(field => {
          const errorMessages = error.response.data[field];
          if (errorMessages && errorMessages.length > 0) {
            // Aquí puedes manejar los errores específicos de cada campo si es necesario
          }
        });
      }
    }
  };

  useEffect(() => {
    setBlinkMessage(''); // Inicializa el mensaje de parpadeo
  }, []);

  return (
    <div className="container-grid-login">
      <div className="form-section">
        <div className="form-container">
          <h3>Iniciar Sesión</h3>
          <br />
          <div id="blinkMessageContainer" style={{ color: 'red', marginBottom: '10px' }}>
            {blinkMessage} {/* El mensaje se actualiza dinámicamente */}
          </div>
          <p id="accessoriesMessage"></p>

          <div id="tab1" className={`tab-content ${activeTab === 1 ? 'tab-active' : ''}`}>
            <form onSubmit={(e) => e.preventDefault()}>
              <label>Nombre de Usuario:</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
              <div id="blinkMessageError"></div>
            </form>
          </div>

          <div id="tab2" className={`tab-content ${activeTab === 2 ? 'tab-active' : ''}`}>
            <h3 id="blinkMessage">Parpadea 3 veces para registrar tu rostro</h3>
            <div className="oval-camera">
              <video id="video" className="hidden" autoPlay playsInline></video>
              <canvas id="canvas"></canvas>
            </div>
          </div>

          <div className="tab-buttons">
            {activeTab === 2 && (
              <button className="btn-primary" type="button" onClick={previousTab}>
                Anterior
              </button>
            )}
            {activeTab === 1 && (
              <button
                className="btn-primary"
                type="button"
                id="nextTabButton"
                onClick={nextTab}>Siguiente
              </button>
            )}
          </div>
          <div className="registration-prompt">
            <label>Aún no tienes cuenta? <a href="/register" className="link_register">¡Crea una aquí!</a></label>
          </div >
        </div>

      </div>
    </div>
  );
}
