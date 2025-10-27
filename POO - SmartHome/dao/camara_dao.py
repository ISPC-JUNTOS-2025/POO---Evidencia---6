from dao.interfaces.i_camara_dao import ICamaraDAO
from dominio.camara import Camara
from conn.db_conn import DBConn
import mysql.connector


class CamaraDAO(ICamaraDAO):
    
    def crear(self, camara: Camara):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_general = """
                    INSERT INTO dispositivos (nombre, marca, modelo, consumo_energetico, tipo_dispositivo, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                datos_generales = (
                    camara.get_nombre(),
                    camara.get_marca(),
                    camara.get_modelo(),
                    camara.get_consumo_energetico(),
                    camara.get_tipo_dispositivo().value,
                    camara.get_id_usuario()
                )
                cursor.execute(query_general, datos_generales)
                id_dispositivo = cursor.lastrowid

                query_especifica = """
                    INSERT INTO camara (id_dispositivo, resolucion, vision_nocturna, grabacion, almacenamiento_local)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_especifica, (
                    id_dispositivo,
                    camara.get_resolucion(),
                    camara.get_vision_nocturna(),
                    camara.get_grabacion(),
                    camara.get_almacenamiento_local()
                ))
                
                conn.commit()
                return id_dispositivo
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al crear camara: {error}")

    def buscar_por_id(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, c.resolucion, c.vision_nocturna, c.grabacion, c.almacenamiento_local
                    FROM dispositivos d
                    INNER JOIN camara c ON d.id_dispositivo = c.id_dispositivo
                    WHERE d.id_dispositivo = %s
                """
                cursor.execute(query, (id_dispositivo,))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar camara por ID: {error}")

    def buscar_por_usuario(self, id_usuario: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, c.resolucion, c.vision_nocturna, c.grabacion, c.almacenamiento_local
                    FROM dispositivos d
                    INNER JOIN camara c ON d.id_dispositivo = c.id_dispositivo
                    WHERE d.id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar camaras por usuario: {error}")

    def buscar_todas(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, c.resolucion, c.vision_nocturna, c.grabacion, c.almacenamiento_local
                    FROM dispositivos d
                    INNER JOIN camara c ON d.id_dispositivo = c.id_dispositivo
                """
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al listar todas las camaras: {error}")

    def actualizar(self, camara: Camara):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_dispositivo = """
                    UPDATE dispositivos 
                    SET nombre=%s, marca=%s, modelo=%s, consumo_energetico=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_dispositivo, (
                    camara.get_nombre(),
                    camara.get_marca(),
                    camara.get_modelo(),
                    camara.get_consumo_energetico(),
                    camara.get_id_dispositivo()
                ))
                
                query_camara = """
                    UPDATE camara 
                    SET resolucion=%s, vision_nocturna=%s, grabacion=%s, almacenamiento_local=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_camara, (
                    camara.get_resolucion(),
                    camara.get_vision_nocturna(),
                    camara.get_grabacion(),
                    camara.get_almacenamiento_local(),
                    camara.get_id_dispositivo()
                ))
                
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar camara: {error}")

    def eliminar(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "DELETE FROM dispositivos WHERE id_dispositivo = %s"
                cursor.execute(query, (id_dispositivo,))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al eliminar camara: {error}")

    def actualizar_resolucion(self, id_dispositivo: int, resolucion: str):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE camara SET resolucion = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (resolucion, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar resolucion: {error}")

    def actualizar_vision_nocturna(self, id_dispositivo: int, vision_nocturna: bool):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE camara SET vision_nocturna = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (vision_nocturna, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar vision nocturna: {error}")

    def actualizar_grabacion(self, id_dispositivo: int, grabacion: bool):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE camara SET grabacion = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (grabacion, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar grabacion: {error}")
