# Smart Home Database — Evidencia 6

## Motor de base de datos utilizado
El proyecto fue desarrollado usando MySQL 8 como motor principal.

## Cómo ejecutar el script

1. Ingresar a [https://onecompiler.com/mysql](https://onecompiler.com/mysql)
2. Seleccionar el lenguaje *MySQL*.
3. Copiar y pegar el contenido del archivo primero el ddl_smart_home_db.sql junto con dml_smart_home_db.sql (Se pueden pegar ambos archivos uno debajo del otro en el mismo editor).
4. Ejecutar el código para visualizar los resultados de las consultas.

## Contenido de los script
El archivo ddl_smart_home_db incluye la creacion de las tablas con sus respectivos campos:
 - usuarios, dispositivos, camara, automatizaciones etc 

El archivo dml_smart_home_db incluye todo lo necesario para probar la base de datos:
- Inserciones (INSERT) para poblar las tablas con datos de ejemplo: usuarios, dispositivos, sensores, automatizaciones y eventos.
- Consultas multitabla (JOIN) que muestran relaciones reales entre los datos (por ejemplo, qué dispositivos tiene cada usuario o qué automatización controla qué aparato).
- *Subconsultas* que responden a preguntas más específicas del sistema, como cuántos dispositivos tiene cada usuario o qué dispositivos pertenecen al administrador.
- Comentarios descriptivos que explican el propósito de cada consulta.
