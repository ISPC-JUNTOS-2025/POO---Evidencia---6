from dao.interfaces.i_sensor_movimiento_dao import ISensorMovimientoDAO
from dominio.sensor_movimiento import SensorMovimiento
from datetime import datetime
from conn.db_conn import DBConn
import mysql.connector


class SensorMovimientoDAO(ISensorMovimientoDAO):
    
    def crear(self, sensor: SensorMovimiento):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_general = """
                    INSERT INTO dispositivos (nombre, marca, modelo, consumo_energetico, tipo_dispositivo, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                datos_generales = (
                    sensor.get_nombre(),
                    sensor.get_marca(),
                    sensor.get_modelo(),
                    sensor.get_consumo_energetico(),
                    sensor.get_tipo_dispositivo().value,
                    sensor.get_id_usuario()
                )
                cursor.execute(query_general, datos_generales)
                id_dispositivo = cursor.lastrowid

                query_especifica = """
                    INSERT INTO sensor_movimiento (id_dispositivo, estado_activo, ultima_deteccion)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_especifica, (
                    id_dispositivo,
                    sensor.get_estado_activo(),
                    sensor.get_ultima_deteccion()
                ))
                
                conn.commit()
                return id_dispositivo
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al crear sensor de movimiento: {error}")

    def buscar_por_id(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, s.estado_activo, s.ultima_deteccion
                    FROM dispositivos d
                    INNER JOIN sensor_movimiento s ON d.id_dispositivo = s.id_dispositivo
                    WHERE d.id_dispositivo = %s
                """
                cursor.execute(query, (id_dispositivo,))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar sensor por ID: {error}")

    def buscar_por_usuario(self, id_usuario: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, s.estado_activo, s.ultima_deteccion
                    FROM dispositivos d
                    INNER JOIN sensor_movimiento s ON d.id_dispositivo = s.id_dispositivo
                    WHERE d.id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar sensores por usuario: {error}")

    def buscar_todas(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, s.estado_activo, s.ultima_deteccion
                    FROM dispositivos d
                    INNER JOIN sensor_movimiento s ON d.id_dispositivo = s.id_dispositivo
                """
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al listar todos los sensores: {error}")

    def actualizar(self, luz: Luz):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_dispositivo = """
                    UPDATE dispositivos 
                    SET nombre=%s, marca=%s, modelo=%s, consumo_energetico=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_dispositivo, (
                    sensor.get_nombre(),
                    sensor.get_marca(),
                    sensor.get_modelo(),
                    sensor.get_consumo_energetico(),
                    sensor.get_id_dispositivo()
                ))
                
                query_luz = """
                    UPDATE sensor_movimiento 
                    SET intensidad=%s, regulable=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_luz, (
                    sensor.get_estado_activo(),
                    sensor.get_ultima_deteccion(),
                    sensor.get_id_dispositivo()
                ))
                
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar sensor: {error}")

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
                raise Exception(f"Error al eliminar sensor: {error}")

    def actualizar_estado_activo(self, id_dispositivo: int, estado_activo: bool):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE sensor_movimiento SET estado_activo = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (estado_activo, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar estado activo: {error}")

    def registrar_deteccion(self, id_dispositivo: int, fecha_deteccion):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE sensor_movimiento SET ultima_deteccion = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (fecha_deteccion, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al registrar deteccion: {error}")

    def buscar_detecciones_por_sensor(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT ultima_deteccion
                    FROM sensor_movimiento
                    WHERE id_dispositivo = %s AND ultima_deteccion IS NOT NULL
                """
                cursor.execute(query, (id_dispositivo,))
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar detecciones por sensor: {error}")
