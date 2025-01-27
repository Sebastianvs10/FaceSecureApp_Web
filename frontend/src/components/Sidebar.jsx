import React, { useState } from 'react';

const Sidebar = ({ role }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Maneja la expansión y compresión del sidebar
  return (
    <nav
      id="sidebar"
      className={isSidebarOpen ? 'open' : ''}
      onMouseEnter={() => setIsSidebarOpen(true)} // Expande el sidebar cuando el cursor entra
      onMouseLeave={() => setIsSidebarOpen(false)} // Comprime el sidebar cuando el cursor sale
    >
      <div className="sidebar-content">
        <a href="/dashboard">
          <i className="fa-solid fa-house"></i>
          {isSidebarOpen && <span>Inicio</span>} {/* Mostrar texto solo cuando el sidebar está abierto */}
        </a>
        {role === 'Admin' && (
          <a href="/adminusers">
            <i className="fa-solid fa-users-cog"></i>
            {isSidebarOpen && <span>Gestionar usuarios</span>} {/* Mostrar texto solo cuando el sidebar está abierto */}
          </a>
        )}
      </div>
    </nav>
  );
};

export default Sidebar;
