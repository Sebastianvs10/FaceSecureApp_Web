import React from 'react';
import '../index.css'; // Assuming your CSS file is in the same folder

const Index = () => {
  return (
      <div className="container-grid">
        {/* Left side with image */}
        <div className="image-section">
          <img src="../../public/images/facial_recognition_animation.gif" alt="Image" className="responsive-image" />
        </div>
        {/* Right side with action buttons */}
        <div className="form-section">
          <div className="form-container">
            <h2>Bienvenido de nuevo</h2>
            <img src="../../public/images/reconocimiento-facial.png" width="150" height="150" className="responsive-image" />

            {/* Login Button */}
            <form action="/login" method="get">
              <button type="submit" className="btn-primary">Iniciar sesión</button>
            </form>

            <br />

            {/* Register Button */}
            <form action="/register" method="get">
              <label>Aún no estás registrado?
                <a href="/register" className="link_register"> Registrate</a>
              </label>
            </form>
          </div>
        </div>
      </div>
  );
};

export default Index;
