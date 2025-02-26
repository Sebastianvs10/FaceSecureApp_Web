# 🚀 Proyecto de Autenticación Biométrica Facial - FaceSecureApp

**FaceSecureApp** es una aplicación de autenticación biométrica facial que utiliza un sistema de reconocimiento facial para verificar la identidad de los usuarios. El proyecto está compuesto por un backend desarrollado con **Django** y un frontend construido con **React**, mientras que **PostgreSQL** se usa para almacenar los datos de los usuarios y registros faciales.

## 📝 Descripción

El proyecto permite que los usuarios se registren utilizando su rostro y autentiquen su identidad mediante una cámara. La base de datos almacena las imágenes faciales y la información del usuario. El sistema utiliza **OpenCV**, **FaceRecognition** y **Django** para el procesamiento de imágenes y autenticación.

### ⚙️ Características:
- **👤 Registro de usuarios**: Captura la imagen facial y la almacena en la base de datos.
- **🔒 Autenticación facial**: Compara las imágenes faciales registradas con la imagen en tiempo real para autenticar a los usuarios.
- **🌐 Interfaz de usuario React**: Una interfaz interactiva para facilitar el proceso de autenticación.

## 🛠️ Tecnologías utilizadas

- **Backend**: Django con Django REST Framework para crear la API.
- **Frontend**: React para la interfaz de usuario.
- **Base de datos**: PostgreSQL para almacenar los datos de los usuarios y las imágenes faciales.
- **Librerías**:
  - **🖼️ OpenCV**: Para procesamiento de imágenes.
  - **🧠 TensorFlow / Keras / FaceRecognition**: Para redes neuronales en la autenticación facial.

## 🧑‍💻 Requisitos

Asegúrate de tener los siguientes requisitos instalados en tu máquina:

- [🐍 Python 3.8+](https://www.python.org/downloads/)
- [🔧 Node.js](https://nodejs.org/) (preferiblemente la versión LTS).
- [📦 npm](https://www.npmjs.com/) o [🧶 yarn](https://yarnpkg.com/) para el frontend.
- [📚 PostgreSQL](https://www.postgresql.org/) instalado y en funcionamiento.
- [🌐 Django](https://www.djangoproject.com/) y [Django REST Framework](https://www.django-rest-framework.org/) para el backend.

## 🚀 Pasos para ejecutar el proyecto

### 1. 📥 Clonar el repositorio

Primero, clona el repositorio desde GitHub:

```bash
git clone https://github.com/Sebastianvs10/FaceSecureApp_Web
```
### 2. 📂 Navegar a la carpeta del proyecto

Accede al directorio del proyecto clonado:
```bash
cd FaceSecureApp_Web
```

### 3. 🛠️ Configurar la base de datos PostgreSQL
```bash
psql -U postgres
CREATE DATABASE face_secure_db;
```

### 4. ⚙️ Configurar el backend (Django)
#### 4.1. 🐍 Instalar las dependencias de Django
Accede a la carpeta del backend y crea un entorno virtual para el proyecto Django:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
```
Instala las dependencias de Django y otras librerías necesarias:

```bash
pip install -r requirements.txt
```
#### 4.3. 🗃️ Ejecutar las migraciones
Aplica las migraciones para configurar la base de datos:
```bash
python manage.py migrate
```
#### 4.4. 🚀 Iniciar el servidor de desarrollo de Django
Inicia el servidor de desarrollo de Django:
```bash
python manage.py runserver
```
El servidor backend estará disponible en http://127.0.0.1:8000. 

### 5. ⚛️ Configurar el frontend (React)
#### 5.1. 📦 Instalar las dependencias del frontend
Accede a la carpeta del frontend (React) y instala las dependencias:
```bash
cd ../frontend
npm install
```
#### 5.3. 🚀 Iniciar el servidor de desarrollo de React
Inicia el servidor de desarrollo de React:
```bash
npm run dev
```
El frontend estará disponible en http://localhost:3000.

### 6. 🌐 Acceder a la aplicación
Una vez que tanto el frontend como el backend estén en funcionamiento, puedes acceder a la aplicación a través de tu navegador en:  

### 7. 🧑‍💻 Registro y autenticación
#### 1. 📝 Registrar un usuario: Utiliza la cámara para capturar la imagen facial y registra un nuevo usuario.
#### 2. 🔒 Autenticación facial: Después de registrar un usuario, puedes usar la cámara para intentar autenticarte comparando tu rostro con el que está registrado en la base de datos.


## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
