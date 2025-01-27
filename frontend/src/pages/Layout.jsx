import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";

export default function Layout() {
  const location = useLocation();

  // Definir las rutas donde no queremos mostrar el layout (ej. login, register)
  const noLayoutPaths = ['/login', '/register'];

  // Si la ruta actual es una de las definidas en `noLayoutPaths`, no mostramos el layout con navegación
  if (noLayoutPaths.includes(location.pathname)) {
    return <Outlet />;
  }

  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/register">Register</Link>
          </li>
        </ul>
      </nav>
      <Outlet /> {/* Aquí se renderiza el contenido de la ruta específica */}
    </>
  );
}
