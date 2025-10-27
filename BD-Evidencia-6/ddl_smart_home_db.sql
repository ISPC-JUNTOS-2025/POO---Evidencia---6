CREATE DATABASE IF NOT EXISTS smart_home_db;
USE smart_home_db;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'usuario', 'invitado') NOT NULL DEFAULT 'usuario',
    calle VARCHAR(200) NOT NULL,
    numero INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE dispositivos (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    activado BOOLEAN DEFAULT FALSE,
    consumo_energetico DECIMAL(10,2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_dispositivo ENUM('Luz', 'Electrodomestico', 'Sensor', 'Dispositivo De Grabacion') NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);


CREATE TABLE aire_acondicionado (
    id_dispositivo INT PRIMARY KEY,
    temperatura_objetivo INT NOT NULL,
    modo_eco BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE
);

CREATE TABLE camara (
    id_dispositivo INT PRIMARY KEY,
    resolucion ENUM('720p', '1080p', '2K', '4K') NOT NULL DEFAULT '1080p',
    vision_nocturna BOOLEAN DEFAULT TRUE,
    grabacion BOOLEAN DEFAULT FALSE,
    almacenamiento_local BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE
);

CREATE TABLE sensor_movimiento (
    id_dispositivo INT PRIMARY KEY,
    estado_activo BOOLEAN DEFAULT FALSE,
    ultima_deteccion TIMESTAMP NULL,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE
);

CREATE TABLE luz (
    id_dispositivo INT PRIMARY KEY,
    intensidad INT NOT NULL,
    regulable BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE
);

CREATE TABLE automatizaciones (
    id_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    estado BOOLEAN DEFAULT FALSE,
    regla TEXT NOT NULL,
    condicion TEXT NOT NULL,
    accion TEXT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE automatizacion_dispositivos (
    id_automatizacion INT NOT NULL,
    id_dispositivo INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_automatizacion, id_dispositivo),
    FOREIGN KEY (id_automatizacion) REFERENCES automatizaciones(id_automatizacion) ON DELETE CASCADE,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE
);

CREATE TABLE detecciones_movimiento (
    id_deteccion INT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    nombre_sensor VARCHAR(100) NOT NULL,
    fecha_deteccion TIMESTAMP NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE eventos_dispositivos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    tipo_evento ENUM('encendido', 'apagado', 'cambio_temperatura', 'cambio_intensidad', 'inicio_grabacion', 'fin_grabacion', 'deteccion_movimiento') NOT NULL,
    descripcion TEXT,
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);
