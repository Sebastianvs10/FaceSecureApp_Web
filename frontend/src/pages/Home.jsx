/* Autor: Jhohan Sebastian Vargas S
   // Fecha: 2025-02-25
   # Project: FaceSecureApp
*/

import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {toast} from 'react-toastify';
import Header from '../components/Header.jsx';
import Sidebar from '../components/Sidebar.jsx';
import {useNavigate} from 'react-router-dom'; // Importar hook de redirección

export default function Home() {
  const [name_user, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Control de estado del sidebar
  const navigate = useNavigate(); // Redirigir al login si no está logueado

  // Verificar si el usuario está logueado
  useEffect(() => {
    const checkLoggedInUser = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (token) {
          const config = {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          };
          const response = await axios.get('http://127.0.0.1:8000/api/user/', config);
          setLoggedIn(true);
          setUsername(response.data.name_user);
          setRole(response.data.role);
        } else {
          setLoggedIn(false);
          setUsername('');
          toast.error('¡Vuelva a Iniciar Sesión!');
          navigate('/'); // Redirigir al login

        }
      } catch (error) {
        setLoggedIn(false);
        setUsername('');
        //toast.error('¡Vuelva a Iniciar Sesión!');

        navigate('/'); // Redirigir al login
        toast.error('Su sesión ha expirado, vuelva a iniciar sesión!');
      }
    };
    checkLoggedInUser();
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
        setUsername('');
        toast.success('Sesión Cerrada!');
        navigate('/');  // Redirigir a la página de inicio
      }
    } catch (error) {
      console.error('Failed to logout', error.response?.data || error.message);
    }
  };

  // Función para alternar el estado del sidebar (comprimir/expandir)
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

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
      {isLoggedIn ? (
        <div className="form-container">
          <h2>Hola, {name_user}. Bienvenido!</h2>
        </div>
      ) : null} {/* Si no está logueado, no se muestra nada */}
    </div>
  );
}
