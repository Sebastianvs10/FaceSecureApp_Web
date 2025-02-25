/* Autor: Jhohan Sebastian Vargas S
   // Fecha: 2025-02-25
   # Project: FaceSecureApp
*/

import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {getUserInfo} from '../js/userService.js';
import Header from "../components/Header.jsx";
import Sidebar from "../components/Sidebar.jsx"; // Importa el servicio

const AccountUser = () => {
  const [userData, setUserData] = useState(null);
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Control de estado del sidebar
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (token) {
          // Obtener el ID del usuario logueado desde la API
          const userResponse = await axios.get('http://127.0.0.1:8000/api/user/', {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          const userId = userResponse.data.id;  // Suponiendo que la respuesta tiene un campo 'id'

          // Obtener la información del usuario usando su ID
          const response = await getUserInfo(userId, token);  // Ahora pasamos el ID real
          setUserData(response);
          setLoading(false);
        } else {
          setError('No se ha encontrado el token de autenticación');
          navigate('/login');
          toast.error('¡Vuelva a Iniciar Sesión!');
        }
      } catch (err) {
        setError('Hubo un error al obtener los datos del usuario');
        setLoading(false);
      }
    };
    fetchUserData();
  }, [navigate]);

  // Manejar el cierre de sesión
  const handleLogout = async () => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const refreshToken = localStorage.getItem('refreshToken');
      if (accessToken && refreshToken) {
        const config = {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        };
        await axios.post('http://127.0.0.1:8000/api/logout/', { refresh: refreshToken }, config);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setLoggedIn(false);
        toast.success('Sesión Cerrada!');
        navigate('/');  // Redirigir a la página de inicio
      }
    } catch (error) {
      console.error('Failed to logout', error.response?.data || error.message);
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  // Extraemos la información del usuario
  const { username, user_code, name_user, role, email, face_data } = userData;

  return (
    <div>
      {/* Header */}
      <Header
        name_user={name_user}
        role={role}
        onLogout={handleLogout}
        onToggleSidebar={toggleSidebar} // Pasar la función de alternar sidebar
      />

      {/* Sidebar */}
      <Sidebar
        isSidebarOpen={isSidebarOpen}
        role={role}
      />

      {/* Contenido principal */}
      <div className="account-user container">
        <h2>Mi cuenta</h2>

        <div className="profile-info">
          {/* Imagen del rostro */}
          {face_data && (
            <div className="profile-field">
              <div className="image-container">
                <img src={face_data} alt="Imagen de rostro" className="profile-image" />
              </div>
            </div>
          )}

          {/* Información del usuario */}
          <div className="profile-field">
            <strong htmlFor="modalUserName">Nombre de Usuario:</strong>
            <input type="text" id="modalUserName" className="modal-text" value={name_user} readOnly />
          </div>
          <div className="profile-field">
            <strong htmlFor="modalUserName">Usuario:</strong>
            <input type="text" id="modalUserName" className="modal-text" value={username} readOnly />
          </div>
          <div className="profile-field">
            <strong htmlFor="modalUserCode">Código de Usuario:</strong>
            <input type="text" id="modalUserCode" className="modal-text" value={user_code} readOnly />
          </div>
          <div className="profile-field">
            <strong htmlFor="modalUserRole">Rol:</strong>
            <input type="text" id="modalUserRole" className="modal-text" value={role} readOnly />
          </div>
          <div className="profile-field">
            <strong htmlFor="modalUserEmail">Correo Electrónico:</strong>
            <input type="email" id="modalUserEmail" className="modal-text" value={email} readOnly />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountUser;
