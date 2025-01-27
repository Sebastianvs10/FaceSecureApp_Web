import React, { useState } from 'react';

const Header = ({ name_user, role, onLogout, onToggleSidebar }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Función para obtener las iniciales del nombre
  const getInitials = (name) => {
    const names = name.split(' ');
    const initials = names.map((namePart) => namePart.charAt(0).toUpperCase()).join('');
    return initials;
  };

  // Función para mostrar el dropdown al pasar el cursor sobre las iniciales
  const handleMouseEnter = () => {
    setIsDropdownOpen(true);
  };

  // Función para ocultar el dropdown cuando el cursor se va
  const handleMouseLeave = () => {
    setIsDropdownOpen(false);
  };

  // Función para manejar clics dentro del dropdown
  const handleDropdownClick = (e) => {
    e.stopPropagation(); // Evita que el clic cierre el dropdown
  };

  return (
    <header>
      {/* Botón para el menú lateral */}
      <span className="toggle-menu" onClick={onToggleSidebar}>☰</span>

      {/* Sección con las iniciales */}
      <div className="user-info-container">
        <span
          className="initials"
          onMouseEnter={handleMouseEnter} // Mostrar el dropdown al pasar el cursor
          onMouseLeave={handleMouseLeave} // Ocultar el dropdown cuando el cursor se va
        >
          {getInitials(name_user)} {/* Mostrar las iniciales del nombre */}
        </span>

        {/* Dropdown que muestra el nombre completo y las opciones */}
        {isDropdownOpen && (
          <div
            className="dropdown"
            onMouseEnter={handleMouseEnter} // Mostrar el dropdown al pasar el cursor
            onMouseLeave={handleMouseLeave} // Ocultar el dropdown cuando el cursor se va
            onClick={handleDropdownClick} // Evitar que el dropdown se cierre al hacer clic dentro
          >
            <h3>{name_user}</h3> {/* Nombre completo */}
            <h4>Perfil: {role}</h4>
            <br/>
            <a href="/account">
              <i className="fa-solid fa-user-gear" style={{ color: '#e6410a', fontSize: '20px' }}></i>
              Mi cuenta
            </a> {/* Opción de ver cuenta */}
            <a onClick={onLogout}>
              <i className="fa-solid fa-right-from-bracket" style={{color: '#ff0000', fontSize: '20px'}}></i>
              Cerrar sesión
            </a> {/* Opción de cerrar sesión */}
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
