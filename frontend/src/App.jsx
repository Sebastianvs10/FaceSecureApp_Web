import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {ToastContainer} from 'react-toastify';
import Home from "./pages/Home"
import Layout from './pages/Layout';
import Register from './pages/Register';
import Login from './pages/Login'
import Index from './pages/Index'
import AdminUsers from "./pages/AdminUsers.jsx";
import AccessUser from "./pages/AccessUser.jsx"
import '@fortawesome/fontawesome-free/css/all.css';
import AccountUser from "./pages/accountUser.jsx";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Index />} />
          <Route path="dashboard" element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="adminusers" element={<AdminUsers />} />
          <Route path="account" element={<AccountUser />} />
          <Route path="access" element={<AccessUser />} />
        </Route>
      </Routes>
      {/* Configura el ToastContainer para mostrar los Toasts en la parte inferior derecha */}
      <ToastContainer
        position="bottom-right" // Establece la posición en la parte inferior derecha
        autoClose={5000} // Tiempo en milisegundos para cerrar automáticamente
        hideProgressBar={false} // Mostrar barra de progreso
        newestOnTop={true} // Los nuevos Toasts aparecen encima de los anteriores
        closeButton={true} // Habilita el botón de cerrar en los Toasts
        rtl={false} // Desactiva el soporte de RTL
        pauseOnFocusLoss={true} // Pausa el Toast cuando la página pierde el foco
        draggable={true} // Permite arrastrar el Toast
        pauseOnHover={true} // Pausa el Toast cuando se pasa el ratón sobre él
      />
    </BrowserRouter>
  );
}


export default App
