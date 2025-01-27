FROM node:alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app/

# Instalar dependencias
RUN npm install

# Crear la build de producción
RUN npm run build

# Servir la aplicación en producción usando un servidor estático (por ejemplo, `serve`)
RUN npm install -g serve

# Exponer el puerto en el que se servirá el frontend
EXPOSE 3000
EXPOSE 5173

# Comando para ejecutar el frontend
CMD ["serve", "-s", "build", "-l", "3000"]
