import React, {useEffect, useRef, useState} from 'react';

const Header = ({ name_user, role, onLogout, onToggleSidebar }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null); // Referencia para el dropdown

  // Función para obtener las iniciales del nombre
  const getInitials = (name) => {
    const names = name.split(' ');
    const initials = names.map((namePart) => namePart.charAt(0).toUpperCase()).join('');
    return initials;
  };

  // Función para toggle del dropdown al hacer clic
  const handleToggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  // Función para cerrar el dropdown al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };

    // Agregar el event listener al documento
    document.addEventListener('mousedown', handleClickOutside);

    // Limpiar el event listener al desmontar el componente
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <header>
      {/* Botón para el menú lateral */}
      <span className="toggle-menu" onClick={onToggleSidebar}>☰</span>

      {/* Sección con las iniciales */}
      <div className="user-info-container" ref={dropdownRef}>
        <span
          className="initials"
          onClick={handleToggleDropdown} // Toggle al hacer clic
        >
          {getInitials(name_user)} {/* Mostrar las iniciales del nombre */}
        </span>

        {/* Dropdown que muestra el nombre completo y las opciones */}
        {isDropdownOpen && (
          <div className="dropdown">
            <div className="info_user">
              <p>{name_user}</p> {/* Nombre completo */}
              <p>Perfil: {role}</p>
            </div>

            <a href="/account">
              <i className="fa-solid fa-user-gear" style={{ color: '#e6410a', fontSize: '20px', marginRight: '6px', marginLeft: '6px' }}></i>
              Mi cuenta
            </a> {/* Opción de ver cuenta */}
            <a onClick={onLogout}>
              <i className="fa-solid fa-right-from-bracket" style={{ color: '#ff0000', fontSize: '20px', marginRight: '8px', marginLeft: '6px'   }}></i>
              Cerrar sesión
            </a> {/* Opción de cerrar sesión */}
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;