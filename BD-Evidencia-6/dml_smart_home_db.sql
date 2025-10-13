USE smart_home_db;

-- Tabla: usuarios
INSERT INTO usuarios (nombre, apellido, email, contraseña, rol, calle, numero) VALUES
('Juan', 'Pérez', 'juanperez@gmail.com', '+-=@$x@bsx¿', 'administrador', 'Av. General paz', 742),
('María', 'Gómez', 'mariagomez@gmail.com', 'asjdnsc8', 'usuario', 'San Martín', 120),
('Carlos', 'López', 'carloslopez@gmail.com', 'asjsnj8s74fa', 'usuario', 'Belgrano', 100),
('Lucía', 'Martínez', 'luciamartinez@gmail.com', 'pass', 'usuario', 'Rivadavia', 345),
('Ana', 'Fernández', 'anafernandez@gmail.com', 'pass', 'invitado', 'Mitre', 678),
('Pedro', 'Suárez', 'pedrosuarez@gmail.com', '1258418a', 'usuario', 'Hernandarias', 5612),
('Sofía', 'Torres', 'sofiatorres@gmail.com', 'qwertysn4', 'usuario', 'Pueyrredón', 7891),
('Nicolás', 'Ruiz', 'nicolasruiz@gmail.com', 'asds68f', 'usuario', 'riobamba', 321),
('Laura', 'Cruz', 'lauracruz@gmail.com', 'pass', 'usuario', 'Saavedra', 888),
('Diego', 'Silva', 'diegosilva@gmail.com', 'pass', 'usuario', 'Córdoba', 939);

-- Tabla: dispositivos
INSERT INTO dispositivos (nombre, marca, modelo, activado, consumo_energetico, tipo_dispositivo, id_usuario) VALUES
('Luz Living', 'Philips', 'Hue123', TRUE, 10.5, 'Luz', 1),
('Luz Cocina', 'Xiaomi', 'MiLight', FALSE, 8.2, 'Luz', 2),
('Aire Principal', 'Samsung', 'WindFree', TRUE, 1500, 'Electrodomestico', 1),
('Cámara Entrada', 'Logitech', 'C920', TRUE, 5.0, 'Dispositivo De Grabacion', 1),
('Sensor Movimiento Garage', 'Xiaomi', 'SMv2', TRUE, 2.0, 'Sensor', 1),
('Cámara Living', 'Panacom', 'HK1080', TRUE, 5.0, 'Dispositivo De Grabacion', 3),
('Luz Habitación', 'Philips', 'HueMini', FALSE, 6.0, 'Luz', 4),
('Aire Cuarto', 'LG', 'DualCool', FALSE, 1400, 'Electrodomestico', 4),
('Sensor Pasillo', 'Xiaomi', 'SMLight', TRUE, 2.0, 'Sensor', 2),
('Luz Patio', 'Philips', 'Outdoor', TRUE, 9.0, 'Luz', 2),
('Aire Oficina', 'Samsung', 'WindFreeMini', FALSE, 1200, 'Electrodomestico', 2),
('Aire Dormitorio 1', 'LG', 'DualCoolPlus', TRUE, 1400, 'Electrodomestico', 3),
('Aire Dormitorio 2', 'Samsung', 'WindFree', TRUE, 1500, 'Electrodomestico', 4),
('Aire Living', 'Daikin', 'FTXJ', TRUE, 1600, 'Electrodomestico', 1),
('Aire Cocina', 'LG', 'ArtCool', FALSE, 1300, 'Electrodomestico', 2),
('Aire Garage', 'Samsung', 'WindFree', TRUE, 1500, 'Electrodomestico', 3),
('Aire Pasillo', 'LG', 'DualCoolMini', FALSE, 1200, 'Electrodomestico', 4),
('Aire Patio', 'Daikin', 'FTXJ', TRUE, 1600, 'Electrodomestico', 2),
('Luz Habitación 2', 'Philips', 'HueGo', TRUE, 7.0, 'Luz', 3),      
('Luz Baño', 'Xiaomi', 'MiLightMini', FALSE, 5.5, 'Luz', 4),           
('Luz Terraza', 'Philips', 'HueOutdoor', TRUE, 9.5, 'Luz', 5),         
('Luz Cocina 2', 'Xiaomi', 'MiLightPlus', TRUE, 8.0, 'Luz', 6),        
('Luz Living 2', 'Philips', 'HueWhite', FALSE, 6.5, 'Luz', 7),        
('Luz Oficina', 'Xiaomi', 'MiLightPro', TRUE, 7.5, 'Luz', 8),         
('Cámara Cocina', 'Logitech', 'C922', TRUE, 5.0, 'Dispositivo De Grabacion', 2),  
('Cámara Habitación', 'Panacom', 'HK720', TRUE, 4.5, 'Dispositivo De Grabacion', 3), 
('Cámara Oficina', 'Logitech', 'C930', FALSE, 5.0, 'Dispositivo De Grabacion', 4),   
('Cámara Patio', 'Panacom', 'HK1080Pro', TRUE, 6.0, 'Dispositivo De Grabacion', 5), 
('Cámara Garage', 'Logitech', 'C910', TRUE, 5.5, 'Dispositivo De Grabacion', 6),     
('Cámara Living 2', 'Panacom', 'HK1080Plus', FALSE, 5.0, 'Dispositivo De Grabacion', 7), 
('Cámara Entrada 2', 'Logitech', 'C920Pro', TRUE, 5.0, 'Dispositivo De Grabacion', 8),  
('Cámara Terraza', 'Panacom', 'HK720Pro', TRUE, 4.5, 'Dispositivo De Grabacion', 9),  
('Sensor Habitación', 'Xiaomi', 'SMLight2', TRUE, 2.0, 'Sensor', 3),  
('Sensor Cocina', 'Xiaomi', 'SMLight3', TRUE, 2.0, 'Sensor', 4),      
('Sensor Living', 'Xiaomi', 'SMLight4', FALSE, 2.0, 'Sensor', 5),      
('Sensor Oficina', 'Xiaomi', 'SMLight5', TRUE, 2.0, 'Sensor', 6),      
('Sensor Patio', 'Xiaomi', 'SMLight6', TRUE, 2.0, 'Sensor', 7),       
('Sensor Garage 2', 'Xiaomi', 'SMLight7', FALSE, 2.0, 'Sensor', 8),    
('Sensor Pasillo 2', 'Xiaomi', 'SMLight8', TRUE, 2.0, 'Sensor', 9),    
('Sensor Terraza', 'Xiaomi', 'SMLight9', TRUE, 2.0, 'Sensor', 10); 


-- Luz
INSERT INTO luz (id_dispositivo, intensidad, regulable) VALUES
(1, 80, TRUE),
(2, 50, TRUE),
(7, 100, FALSE),
(10, 60, TRUE),
(19, 70, TRUE),
(20, 90, FALSE),
(21, 55, TRUE),
(22, 65, TRUE),
(23, 75, FALSE),
(24, 85, TRUE);

-- Aire acondicionado
INSERT INTO aire_acondicionado (id_dispositivo, temperatura_objetivo, modo_eco) VALUES
(3, 24, TRUE),
(8, 22, FALSE),
(11, 23, TRUE),
(12, 21, FALSE),
(13, 24, TRUE),
(14, 22, FALSE),
(15, 23, TRUE),
(16, 24, FALSE),
(17, 22, TRUE),
(18, 21, FALSE);

-- Cámara
INSERT INTO camara (id_dispositivo, resolucion, vision_nocturna, grabacion, almacenamiento_local) VALUES
(4, '1080p', TRUE, TRUE, TRUE),
(6, '4K', TRUE, FALSE, TRUE),
(25, '1080p', TRUE, TRUE, TRUE),
(26, '4K', FALSE, TRUE, TRUE),
(27, '720p', TRUE, TRUE, FALSE),
(28, '1080p', TRUE, TRUE, TRUE),
(29, '4K', TRUE, TRUE, TRUE),
(30, '1080p', FALSE, TRUE, TRUE),
(31, '1080p', TRUE, FALSE, TRUE),
(32, '4K', TRUE, TRUE, TRUE);

-- Sensor de movimiento
INSERT INTO sensor_movimiento (id_dispositivo, estado_activo, ultima_deteccion) VALUES
(5, TRUE, NOW()),
(9, TRUE, NOW()),
(33, TRUE, NOW()),
(34, FALSE, NOW()),
(35, TRUE, NOW()),
(36, TRUE, NOW()),
(37, FALSE, NOW()),
(38, TRUE, NOW()),
(39, TRUE, NOW()),
(40, FALSE, NOW());

-- Automatizaciones
INSERT INTO automatizaciones (nombre, descripcion, estado, regla, condicion, accion, id_usuario) VALUES
('Encender luces al detectar movimiento', 'Automatiza luces al detectar movimiento', TRUE, 'deteccion_movimiento', 'sensor_activado', 'encender_luz', 1),
('Apagar aire cuando no hay movimiento', 'Modo ahorro energía', TRUE, 'sin_movimiento', 'sensor_inactivo', 'apagar_aire', 1),
('Encender cámara al salir', 'Seguridad', FALSE, 'modo_fuera', 'usuario_ausente', 'activar_camara', 3),
('Apagar luces al amanecer', 'Ahorro energía', TRUE, 'amanecer', 'hora=07:00', 'apagar_luz', 2),
('Activar luces exteriores de noche', 'Seguridad', TRUE, 'anochecer', 'hora=20:00', 'encender_luz', 2),
('Modo descanso', 'Apagar luces y bajar temperatura', FALSE, 'noche', 'hora=23:00', 'apagar_luz_y_bajar_temp', 4),
('Notificar detección', 'Envía notificación por detección', TRUE, 'deteccion', 'sensor_activado', 'enviar_notificacion', 1),
('Apagar todo', 'Apaga todos los dispositivos', FALSE, 'manual', 'usuario_accion', 'apagar_todo', 1),
('Modo vacaciones', 'Activa cámaras y sensores', FALSE, 'modo_vacaciones', 'usuario_fuera', 'activar_camaras_y_sensores', 1),
('Modo invitados', 'Activa luces exteriores', TRUE, 'modo_invitado', 'usuario_presente', 'encender_luz_exterior', 2);


-- Automatización dispositivos
INSERT INTO automatizacion_dispositivos (id_automatizacion, id_dispositivo) VALUES
(1, 5), (1, 1), (2, 8), (3, 4), (5, 10), (6, 7), (7, 9), (8, 3), (9, 6), (10, 2);

-- Detecciones de movimiento
INSERT INTO detecciones_movimiento (id_dispositivo, nombre_sensor, fecha_deteccion, id_usuario) VALUES
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2),
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2),
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2),
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2),
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2);

-- Eventos dispositivos
INSERT INTO eventos_dispositivos (id_dispositivo, tipo_evento, descripcion, id_usuario) VALUES
(1, 'encendido', 'Luz Living encendida automáticamente', 1),
(2, 'encendido', 'Luz Cocina encendida por usuario', 2),
(3, 'cambio_temperatura', 'Aire ajustado a 24°C', 1),
(4, 'inicio_grabacion', 'Grabación iniciada en cámara entrada', 1),
(5, 'deteccion_movimiento', 'Movimiento detectado en garage', 1),
(6, 'inicio_grabacion', 'Cámara Living grabando', 3),
(7, 'apagado', 'Luz habitación apagada', 4),
(8, 'cambio_temperatura', 'Aire cuarto bajado a 22°C', 4),
(9, 'deteccion_movimiento', 'Movimiento en pasillo', 2),
(10, 'encendido', 'Luz patio encendida por automatización', 2);

-- Ver todos los dispositivos ordenados ascendentemente con el nombre del usuario propietario

SELECT d.nombre AS dispositivo, d.tipo_dispositivo, u.nombre AS propietario, u.email
FROM dispositivos d
JOIN usuarios u ON d.id_usuario = u.id_usuario
ORDER BY propietario ASC;

-- Mostrar las automatizaciones y los dispositivos que controlan

SELECT a.nombre AS automatizacion, d.nombre AS dispositivo, d.tipo_dispositivo
FROM automatizaciones a
JOIN automatizacion_dispositivos ad ON a.id_automatizacion = ad.id_automatizacion
JOIN dispositivos d ON ad.id_dispositivo = d.id_dispositivo;

-- Consultar los 5 primeros eventos recientes junto con los usuarios que los generaron
SELECT e.tipo_evento, e.descripcion, e.fecha_evento, u.nombre AS usuario
FROM eventos_dispositivos e
JOIN usuarios u ON e.id_usuario = u.id_usuario
ORDER BY e.fecha_evento DESC
LIMIT 5;

-- Consultar los movimientos detectado

SELECT s.id_dispositivo, s.estado_activo, e.tipo_evento, e.descripcion
FROM sensor_movimiento s
JOIN eventos_dispositivos e ON s.id_dispositivo = e.id_dispositivo
WHERE e.tipo_evento = 'deteccion_movimiento';


-- SUBCONSULTAS
-- Mostrar la cantidad de dispositivos de los usuarios que poseen más de un dispositivo
SELECT nombre, apellido,
       (SELECT COUNT(*) 
        FROM dispositivos d 
        WHERE d.id_usuario = u.id_usuario) AS cantidad_dispositivos
FROM usuarios u
WHERE id_usuario IN (
    SELECT id_usuario 
    FROM dispositivos
    GROUP BY id_usuario
    HAVING COUNT(*) > 1
);


-- Mostrar dispositivo que pertenecen al rol de administrador
SELECT 
    nombre AS dispositivo,
    tipo_dispositivo,
    (SELECT u.nombre FROM usuarios u WHERE u.id_usuario = d.id_usuario) AS nombre_admin,
    (SELECT u.rol FROM usuarios u WHERE u.id_usuario = d.id_usuario) AS rol_admin
FROM dispositivos d
WHERE id_usuario IN (
    SELECT id_usuario 
    FROM usuarios 
    WHERE rol = 'administrador'
);




