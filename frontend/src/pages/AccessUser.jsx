/* Autor: Jhohan Sebastian Vargas S
   // Fecha: 2025-02-25
   # Project: FaceSecureApp
*/

import React, {useEffect, useRef, useState} from 'react';
import axios from 'axios';
import {toast} from 'react-toastify';
import {useNavigate} from 'react-router-dom';
import Header from "../components/Header.jsx";
import Sidebar from "../components/Sidebar.jsx";
import {
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  LineController,
  LineElement,
  PieController,
  PointElement,
  Title,
  Tooltip
} from 'chart.js';

// Registra los componentes necesarios de Chart.js
Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LineController,
  PieController,
  BarController,
  PointElement,
  ArcElement
);

const AccessUser = () => {
  const [accessData, setAccessData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('distance');  // Default is 'distance'
  const navigate = useNavigate();
  const [name_user, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLoggedIn, setLoggedIn] = useState(false);

  const barChartRef = useRef(null);
  const lineChartRef = useRef(null);
  const pieChartRef = useRef(null);

  useEffect(() => {
    const fetchAccessData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('accessToken');
        if (token) {
          const userResponse = await axios.get('http://127.0.0.1:8000/api/user/', {
            headers: { 'Authorization': `Bearer ${token}` },
          });

          const userId = userResponse.data.id;
          const response = await axios.get(`http://127.0.0.1:8000/api/user-info/${userId}`, {
            headers: { 'Authorization': `Bearer ${token}` },
          });

          if (response.data.access_logs) {
            setLoggedIn(true);
            setUsername(response.data.name_user);
            setRole(response.data.role);
            setAccessData(response.data.access_logs);
          } else {
            throw new Error('No se encontraron datos de acceso');
          }
        } else {
          setLoggedIn(false);
          toast.error('¡Vuelva a Iniciar Sesión!');
          setUsername('');
          navigate('/login');
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching access data:', error);
        setError('Error al obtener los datos de accesos');
        setLoading(false);
      }
    };

    fetchAccessData();

    return () => {
      // Limpiar instancias de gráficos
      if (window.barChartInstance) window.barChartInstance.destroy();
      if (window.lineChartInstance) window.lineChartInstance.destroy();
      if (window.pieChartInstance) window.pieChartInstance.destroy();
    };
  }, [navigate]);

  const getGroupedData = (data) => {
    const grouped = {};
    data.forEach((access) => {
      const date = new Date(access.timestamp).toLocaleDateString();
      if (!grouped[date]) {
        grouped[date] = [];
      }
      grouped[date].push(access.distance);
    });

    const labels = [];
    const avgDistances = [];
    for (const [date, distances] of Object.entries(grouped)) {
      labels.push(date);
      const avgDistance = distances.reduce((a, b) => a + b, 0) / distances.length;
      avgDistances.push(avgDistance);
    }

    return { labels, avgDistances };
  };

  const getAccessCountByDay = (data) => {
    const grouped = {};
    data.forEach((access) => {
      const date = new Date(access.timestamp).toLocaleDateString();
      if (!grouped[date]) {
        grouped[date] = 0;
      }
      grouped[date] += 1;
    });

    const labels = Object.keys(grouped);
    const accessCounts = Object.values(grouped);
    return { labels, accessCounts };
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  // Crear los gráficos cuando los datos se actualicen o activeTab cambie
  useEffect(() => {
    if (accessData.length > 0) {
      const { labels, avgDistances } = getGroupedData(accessData);
      const { labels: accessLabels, accessCounts } = getAccessCountByDay(accessData);

      // Limpiar gráficos antes de crear nuevos
      if (window.barChartInstance) window.barChartInstance.destroy();
      if (window.lineChartInstance) window.lineChartInstance.destroy();
      if (window.pieChartInstance) window.pieChartInstance.destroy();

      // Verificar que el canvas de cada gráfico esté disponible
      if (activeTab === 'distance' && barChartRef.current) {
        const barCtx = barChartRef.current.getContext('2d');
        window.barChartInstance = new Chart(barCtx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Distancia Promedio por Día',
              data: avgDistances,
              backgroundColor: 'rgb(210,68,16)',
              borderColor: 'rgba(75,192,192,0.13)',
              borderWidth: 1,
            }],
          },
          options: {
            scales: {
              x: { type: 'category' },
              y: { type: 'linear', beginAtZero: true },
            },
            plugins: {
              title: { display: true, text: 'Distancia Promedio por Día' },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => `${tooltipItem.raw} metros`,
                },
              },
            },
          },
        });
      }

      if (activeTab === 'accesses' && lineChartRef.current) {
        const lineCtx = lineChartRef.current.getContext('2d');
        window.lineChartInstance = new Chart(lineCtx, {
          type: 'line',
          data: {
            labels: accessLabels,
            datasets: [{
              label: 'Accesos por Día',
              data: accessCounts,
              borderColor: 'rgb(210,68,16)',
              fill: false,
            }],
          },
          options: {
            plugins: {
              title: { display: true, text: 'Accesos por Día' },
            },
          },
        });
      }
    }
  }, [accessData, activeTab]);

  const handleLogout = async () => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const refreshToken = localStorage.getItem('refreshToken');
      if (accessToken && refreshToken) {
        const config = {
          headers: { 'Authorization': `Bearer ${accessToken}` },
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
        onToggleSidebar={toggleSidebar}
      />
      <Sidebar isSidebarOpen={isSidebarOpen} role={role} />

      <div className="container-grahp">

        <div className="statistic-tabs">
          <button onClick={() => handleTabClick('distance')}>Distancia Promedio</button>
          <button onClick={() => handleTabClick('accesses')}>Número de Accesos</button>
        </div>

        {loading ? (
          <p>Cargando datos de accesos...</p>
        ) : error ? (
          <p>{error}</p>
        ) : (
          <div className="charts-container">
            {activeTab === 'distance' && (
              <canvas ref={barChartRef} style={{ width: '100%', height: '400px' }}></canvas>
            )}
            {activeTab === 'accesses' && (
              <canvas ref={lineChartRef} style={{ width: '100%', height: '400px' }}></canvas>
            )}
            {activeTab === 'loginDetails' && (
              <canvas ref={pieChartRef} style={{ width: '100%', height: '400px' }}></canvas>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AccessUser;

