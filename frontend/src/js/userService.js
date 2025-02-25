/* Autor: Jhohan Sebastian Vargas S
   // Fecha: 2025-02-25
   # Project: FaceSecureApp
*/

import axios from 'axios';

// Servicio reutilizable para obtener la información del usuario
export const getUserInfo = async (userId, token) => {
  try {
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    };
    const response = await axios.get(`http://127.0.0.1:8000/api/user-info/${userId}/`, config);
    return response.data;
  } catch (error) {
    console.error('Error fetching user info:', error);
    throw error;
  }
};
