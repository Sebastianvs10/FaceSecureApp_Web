import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import Sidebar from "../components/Sidebar.jsx";
import Header from "../components/Header.jsx";

const AdminUsers = () => {
  const [users, setUsers] = useState([]);
  const [totalUsers, setTotalUsers] = useState([]);
  const [userInfo, setUserInfo] = useState(null);
  const [name_user, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);  // Página actual
  const [totalPages, setTotalPages] = useState(1);  // Total de páginas
  const navigate = useNavigate();

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
          fetchUsers(1); // Llamar a la API para obtener usuarios de la primera página
        } else {
          setLoggedIn(false);
          setUsername('');
          toast.error('¡Vuelva a Iniciar Sesión!');
          navigate('/');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setLoggedIn(false);
        setUsername('');
        toast.error('¡Vuelva a Iniciar Sesión!');
        setTimeout(() => {
          navigate('/');
        }, 2000);
      }
    };
    checkLoggedInUser();
  }, [navigate]);

  const fetchUsers = async (page) => {
    try {
      const token = localStorage.getItem('accessToken');
      const config = {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      };
      const response = await axios.get('http://127.0.0.1:8000/api/adminusers/', {
        headers: config.headers,
        params: { page: page, limit: 7 },
      });
      console.log(response.data.results)
      // Verifica si la respuesta contiene 'results' y 'count'
      if (response.data.results && Array.isArray(response.data.results)) {
        setUsers(response.data.results);  // Establecer los usuarios de la página
         setTotalUsers(response.data.count);
        setTotalPages(Math.ceil(response.data.count / 7));  // Calcular el total de páginas
      } else {
        setUsers([]);  // Si la respuesta no tiene 'results', establecer users vacío
      }
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Error al cargar los usuarios');
    }
  };
const fetchUserInfo = (userId) => {
    axios.get(`http://127.0.0.1:8000/api/user-info/${userId}/`)
      .then(response => {
        if (response.data.error) {
          toast.error(response.data.error);
        } else {
          setUserInfo(response.data);
        }
      })
      .catch(error => {
        console.error('Error fetching user info:', error);
        toast.error('Hubo un error al obtener la información del usuario');
      });
  };
  const closeModal = () => {
    setUserInfo(null); // Cerrar el modal limpiando la información del usuario
  };

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
  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    fetchUsers(pageNumber);  // Cargar los usuarios para la página seleccionada
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  // Función para editar el usuario
  const handleEditUser = (userId) => {
    navigate(`/edit-user/${userId}`); // Redirige a la página de edición de usuario
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
      <Sidebar isSidebarOpen={isSidebarOpen} role={role} />

      <div className="container">
        <h2>Administrar Usuarios</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Nombre</th>
              <th>Código</th>
              <th>Email</th>
              <th>Rol</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(users) && users.length > 0 ? (
              users.map((user) => (
                <tr key={user.id} onClick={() => fetchUserInfo(user.id)}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.name_user}</td>
                  <td>{user.user_code}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>
                    <i
                      className="fa fa-pencil-alt"
                      style={{ cursor: 'pointer', fontSize: '18px' }}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditUser(user.id);
                      }}
                    />
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7">No hay usuarios disponibles.</td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Paginación */}
        <div className="pagination">
          {/* Botón de flecha izquierda */}
          <button
            className="btn-pagination"
            disabled={currentPage === 1}
            onClick={() => handlePageChange(currentPage - 1)}
          >
            <i className="fa fa-chevron-left"></i> {/* Icono de flecha izquierda */}
          </button>

          {/* Muestra el rango de registros */}
          <span>{`${(currentPage - 1) * 7 + 1} a ${Math.min(currentPage * 7, totalUsers)} de ${totalUsers}`}</span>

          {/* Botón de flecha derecha */}
          <button
            className="btn-pagination"
            disabled={currentPage === totalPages}
            onClick={() => handlePageChange(currentPage + 1)}
          >
            <i className="fa fa-chevron-right"></i> {/* Icono de flecha derecha */}
          </button>
        </div>
      </div>

      {userInfo && (
        <div id="userModal" className="modal" style={{ display: 'flex' }}>
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <h2>Información del Usuario</h2>

            <div className="modal-flex">
              <div className="modal-left">
                <div className="modal-field">
                  <label htmlFor="modalUserName">Usuario/Correo Electrónico:</label>
                  <input type="text" id="modalUserName" className="modal-text" value={userInfo.email} readOnly />
                </div>

                <div className="modal-field">
                  <label htmlFor="modalUserCode">Código de Usuario:</label>
                  <input type="text" id="modalUserCode" className="modal-text" value={userInfo.user_code} readOnly />
                </div>

                <div className="modal-field">
                  <label htmlFor="modalNameUser">Nombre Usuario:</label>
                  <input type="text" id="modalNameUser" className="modal-text" value={userInfo.name_user} readOnly />
                </div>

                <div className="modal-field">
                  <label htmlFor="modalUserRole">Rol del Usuario:</label>
                  <input type="text" id="modalUserRole" className="modal-text" value={userInfo.role} readOnly />
                </div>

                <img id="modalFaceImage" src={userInfo.face_data || ''} alt="Imagen del rostro" className="modal-image" />
              </div>

              <div>

                <div className="modal-right">
                  <h3>Trazabilidad de Acceso</h3>
                  <table id="accessLogTable">
                    <thead>
                      <tr>
                        <th>Fecha y Hora</th>
                        <th>Éxito</th>
                        <th>Distancia</th>
                      </tr>
                    </thead>
                    <tbody>
                      {userInfo.access_logs?.map((log, index) => (
                        <tr key={index}>
                          <td>{new Date(log.timestamp).toLocaleString()}</td>
                          <td>{log.success ? 'Sí' : 'No'}</td>
                          <td>{log.distance}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <button className="modal-button" onClick={closeModal}>Cerrar</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;
