# Proyecto Smart Home Database

Este proyecto implementa una base de datos relacional para un sistema Smart Home (hogar inteligente), donde se gestionan usuarios, dispositivos conectados, automatizaciones, sensores y eventos de uso. A continuación se describe en detalle cada bloque de inserciones y consultas SQL utilizadas.

## Base de datos utilizada
USE smart_home_db;


Esta línea indica que todas las operaciones se ejecutarán dentro de la base de datos smart_home_db, la cual debe haberse creado previamente. En ella se almacenan todas las tablas necesarias para representar el ecosistema del hogar inteligente.

### Inserciones en la tabla usuarios
INSERT INTO usuarios (nombre, apellido, email, contraseña, rol, calle, numero) VALUES
('Juan', 'Pérez', 'juanperez@gmail.com', '+-=@$x@bsx¿', 'administrador', 'Av. General paz', 742),
('María', 'Gómez', 'mariagomez@gmail.com', 'asjdnsc8', 'usuario', 'San Martín', 120),
...
('Diego', 'Silva', 'diegosilva@gmail.com', 'pass', 'usuario', 'Córdoba', 939);


Aquí se insertan diez usuarios diferentes, cada uno con su nombre, apellido, correo electrónico, contraseña, rol y dirección.
Los roles pueden ser administrador, usuario o invitado, lo que permite distinguir sus permisos dentro del sistema.
El administrador, por ejemplo, puede crear automatizaciones y gestionar dispositivos de otros usuarios.

### Inserciones en la tabla dispositivos
INSERT INTO dispositivos (nombre, marca, modelo, activado, consumo_energetico, tipo_dispositivo, id_usuario) VALUES
('Luz Living', 'Philips', 'Hue123', TRUE, 10.5, 'Luz', 1),
('Luz Cocina', 'Xiaomi', 'MiLight', FALSE, 8.2, 'Luz', 2),
...
('Sensor Terraza', 'Xiaomi', 'SMLight9', TRUE, 2.0, 'Sensor', 10);


Se crean distintos dispositivos inteligentes, como luces, aires acondicionados, cámaras y sensores.
Cada dispositivo pertenece a un usuario (id_usuario), tiene un consumo energético, un tipo específico y un estado de activación (TRUE o FALSE).
Este bloque representa la base del sistema, ya que los dispositivos son los elementos que se controlan y automatizan.

### Inserciones en la tabla luz
INSERT INTO luz (id_dispositivo, intensidad, regulable) VALUES
(1, 80, TRUE),
(2, 50, TRUE),
...
(24, 85, TRUE);


En esta tabla se registran las características propias de los dispositivos tipo luz, como su intensidad y si son regulables.
La columna id_dispositivo actúa como clave foránea que referencia al dispositivo correspondiente en la tabla principal.

### Inserciones en la tabla aire_acondicionado
INSERT INTO aire_acondicionado (id_dispositivo, temperatura_objetivo, modo_eco) VALUES
(3, 24, TRUE),
(8, 22, FALSE),
...
(18, 21, FALSE);


Cada fila representa un aire acondicionado con su temperatura objetivo y si tiene activado el modo ecológico.
Esta información permite controlar el confort térmico y optimizar el consumo energético.

### Inserciones en la tabla camara
INSERT INTO camara (id_dispositivo, resolucion, vision_nocturna, grabacion, almacenamiento_local) VALUES
(4, '1080p', TRUE, TRUE, TRUE),
...
(32, '4K', TRUE, TRUE, TRUE);


Aquí se definen las cámaras de seguridad del sistema, detallando su resolución, capacidad de visión nocturna, si graban automáticamente y si almacenan contenido localmente.
Estas cámaras forman parte de las funciones de seguridad del hogar.

### Inserciones en la tabla sensor_movimiento
INSERT INTO sensor_movimiento (id_dispositivo, estado_activo, ultima_deteccion) VALUES
(5, TRUE, NOW()),
...
(40, FALSE, NOW());


Los sensores de movimiento registran su estado (activo o inactivo) y la última detección de movimiento.
La función NOW() guarda la fecha y hora actual en la que se realiza la inserción, simulando detecciones recientes.

### Inserciones en la tabla automatizaciones
INSERT INTO automatizaciones (nombre, descripcion, estado, regla, condicion, accion, id_usuario) VALUES
('Encender luces al detectar movimiento', 'Automatiza luces al detectar movimiento', TRUE, 'deteccion_movimiento', 'sensor_activado', 'encender_luz', 1),
...
('Modo invitados', 'Activa luces exteriores', TRUE, 'modo_invitado', 'usuario_presente', 'encender_luz_exterior', 2);


Esta tabla define reglas automatizadas que se ejecutan en base a condiciones específicas.
Por ejemplo, una automatización puede encender luces al detectar movimiento o apagar dispositivos al amanecer.
El campo estado indica si la automatización está activa o desactivada, y id_usuario especifica quién la creó.

### Inserciones en la tabla automatizacion_dispositivos
INSERT INTO automatizacion_dispositivos (id_automatizacion, id_dispositivo) VALUES
(1, 5), (1, 1), (2, 8), ...
(10, 2);


Esta tabla intermedia relaciona automatizaciones con dispositivos específicos, permitiendo que una misma regla controle varios aparatos.
Por ejemplo, la automatización “Encender luces al detectar movimiento” afecta tanto al sensor de movimiento como a una luz.

### Inserciones en la tabla detecciones_movimiento
INSERT INTO detecciones_movimiento (id_dispositivo, nombre_sensor, fecha_deteccion, id_usuario) VALUES
(5, 'Sensor Movimiento Garage', NOW(), 1),
(9, 'Sensor Pasillo', NOW(), 2),
...
(9, 'Sensor Pasillo', NOW(), 2);


Se registran los eventos de detección de movimiento ocurridos en diferentes sensores, junto con el usuario al que pertenecen.
La repetición de inserciones simula múltiples detecciones a lo largo del tiempo.

### Inserciones en la tabla eventos_dispositivos
INSERT INTO eventos_dispositivos (id_dispositivo, tipo_evento, descripcion, id_usuario) VALUES
(1, 'encendido', 'Luz Living encendida automáticamente', 1),
...
(10, 'encendido', 'Luz patio encendida por automatización', 2);


Aquí se guardan los eventos generados por los dispositivos, como encendidos, apagados o detecciones.
Estos datos son esenciales para auditoría y análisis del comportamiento del sistema.

## 1 Consultas SQL explicadas
### Ver todos los dispositivos y sus propietarios
SELECT d.nombre AS dispositivo, d.tipo_dispositivo, u.nombre AS propietario, u.email
FROM dispositivos d
JOIN usuarios u ON d.id_usuario = u.id_usuario
ORDER BY propietario ASC;


Esta consulta lista todos los dispositivos junto con el nombre y correo electrónico del usuario propietario.
Se usa una cláusula JOIN para relacionar las tablas dispositivos y usuarios, y se ordena alfabéticamente por el nombre del propietario.

### Mostrar las automatizaciones y los dispositivos que controlan
SELECT a.nombre AS automatizacion, d.nombre AS dispositivo, d.tipo_dispositivo
FROM automatizaciones a
JOIN automatizacion_dispositivos ad ON a.id_automatizacion = ad.id_automatizacion
JOIN dispositivos d ON ad.id_dispositivo = d.id_dispositivo;


Permite visualizar qué dispositivos están vinculados a cada automatización.
Esto refleja la relación muchos a muchos entre ambas entidades.

### Consultar los 5 eventos más recientes
SELECT e.tipo_evento, e.descripcion, e.fecha_evento, u.nombre AS usuario
FROM eventos_dispositivos e
JOIN usuarios u ON e.id_usuario = u.id_usuario
ORDER BY e.fecha_evento DESC
LIMIT 5;


Muestra los cinco eventos más recientes registrados, junto con el nombre del usuario asociado.
La cláusula ORDER BY ... DESC ordena por fecha en orden descendente y LIMIT 5 restringe el resultado.

### Consultar los movimientos detectados
SELECT s.id_dispositivo, s.estado_activo, e.tipo_evento, e.descripcion
FROM sensor_movimiento s
JOIN eventos_dispositivos e ON s.id_dispositivo = e.id_dispositivo
WHERE e.tipo_evento = 'deteccion_movimiento';


Filtra los eventos del tipo detección de movimiento, mostrando los sensores involucrados, su estado y la descripción del evento.
Ideal para analizar la actividad reciente del sistema de seguridad.

## 1 Subconsultas
 ### Mostrar la cantidad de dispositivos por usuario (solo quienes tienen más de uno)
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


Esta consulta anidada calcula cuántos dispositivos posee cada usuario, mostrando únicamente aquellos que tienen más de uno.
Utiliza subconsultas para contar los dispositivos y la cláusula HAVING para aplicar la condición.

### Mostrar dispositivos que pertenecen al rol de administrador
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


Mediante subconsultas se obtiene el nombre y rol del usuario administrador al que pertenece cada dispositivo.
Esto permite verificar qué equipos están bajo control del administrador del sistema.

Conclusión

Este conjunto de comandos SQL construye un entorno completo para un sistema de hogar inteligente, donde se modelan usuarios, dispositivos, sensores, automatizaciones y eventos.
Las consultas permiten analizar el estado general del sistema, sus automatizaciones y la interacción entre los distintos componentes.