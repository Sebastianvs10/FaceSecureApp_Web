import React, { useState } from 'react';
import '../index.css'; // Assuming your CSS file is in the same folder
import { initializeCamera } from '../js/FaceRecognitionFunctions'; // Importar funciones correctamente

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: '',
    user_code: '', // Campo adicional
    name_user: '', // Campo adicional
  });

  const [activeTab, setActiveTab] = useState(1);
  const [blinkMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const nextTab = () => {

    setActiveTab(2);
    // Inicializar la cámara (esto asigna los elementos video y canvas globalmente)
    initializeCamera();
  };

  const previousTab = () => {
    setActiveTab(1);
  };

  return (
    <div className="container-grid-login">
      <div className="form-section">
        <div className="form-container">
          <h3>Registrar Usuario</h3> <br/>
          <div id="blinkMessageContainer" style={{ color: 'red', marginBottom: '10px' }}>
            {blinkMessage} {/* El mensaje se actualiza dinámicamente */}
          </div>
          <div id="tab1" className={`tab-content ${activeTab === 1 ? 'tab-active' : ''}`}>
            <form onSubmit={(e) => e.preventDefault()}> {/* Previene el envío tradicional del formulario */}
              <label>Nombre de Usuario:</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <label>Contraseña:</label>
              <input
                type="password"
                name="password1"
                value={formData.password1}
                onChange={handleChange}
                required
              />
              <label>Confirmar Contraseña:</label>
              <input
                type="password"
                name="password2"
                value={formData.password2}
                onChange={handleChange}
                required
              />
              <label>Código de Usuario:</label>
              <input
                type="text"
                name="user_code"
                value={formData.user_code}
                onChange={handleChange}
                required
              />
              <label>Nombre Completo:</label>
              <input
                type="text"
                name="name_user"
                value={formData.name_user}
                onChange={handleChange}
                required
              />
            </form>
          </div>
          <div id="tab2" className={`tab-content ${activeTab === 2 ? 'tab-active' : ''}`}>
            <h3 id="blinkMessage">Parpadea 3 veces para registrar tu rostro</h3>
            <div className="oval-camera">
              <video id="video" className="hidden" autoPlay playsInline></video> {/* Referencia al video */}
              <canvas id="canvas"></canvas> {/* Referencia al canvas */}
            </div>
          </div>
          <div className="tab-buttons">
            {activeTab === 2 && (
              <button className="btn-primary" type="button" onClick={previousTab}>Anterior</button>
            )}
            {activeTab === 1 && (
              <button className="btn-primary" type="button" onClick={nextTab}>Siguiente</button>
            )}
          </div>

          <div>
           <a href="/" className="btn-primary">Volver al Inicio</a>
          </div>
        </div>
      </div>
    </div>
  );
}