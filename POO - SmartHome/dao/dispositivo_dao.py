from dao.interfaces.i_dispositivo_dao import IDispositivoDAO
from dominio.dispositivo import Dispositivo
from dominio.luz import Luz
from dominio.sensor_movimiento import SensorMovimiento
from dominio.camara import Camara
from dominio.aire_acondicionado import AireAcondicionado
from conn.db_conn import DBConn
import mysql.connector


class DispositivoDAO(IDispositivoDAO):
    
    def crear(self, dispositivo: Dispositivo):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_general = """
                    INSERT INTO dispositivos (nombre, marca, modelo, consumo_energetico, tipo_dispositivo, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                datos_generales = (
                    dispositivo.get_nombre(),
                    dispositivo.get_marca(),
                    dispositivo.get_modelo(),
                    dispositivo.get_consumo_energetico(),
                    dispositivo.get_tipo_dispositivo().value,
                    dispositivo.get_id_usuario()
                )
                cursor.execute(query_general, datos_generales)
                id_dispositivo = cursor.lastrowid

                if isinstance(dispositivo, Luz):
                    query_especifica = """
                        INSERT INTO luz (id_dispositivo, intensidad, regulable)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_intensidad(),
                        dispositivo.get_regulable()
                    ))

                elif isinstance(dispositivo, SensorMovimiento):
                    query_especifica = """
                        INSERT INTO sensor_movimiento (id_dispositivo, sensibilidad, rango)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_sensibilidad(),
                        dispositivo.get_rango()
                    ))

                elif isinstance(dispositivo, Camara):
                    query_especifica = """
                        INSERT INTO camara (id_dispositivo, resolucion, vision_nocturna)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_resolucion(),
                        dispositivo.get_vision_nocturna()
                    ))

                elif isinstance(dispositivo, AireAcondicionado):
                    query_especifica = """
                        INSERT INTO aire_acondicionado (id_dispositivo, temperatura_actual, modo)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_temperatura_actual(),
                        dispositivo.get_modo()
                    ))

                conn.commit()
                return id_dispositivo

            except mysql.connector.Error as error:
                raise Exception(f"Error al crear dispositivo: {error}")


    def buscar_por_nombre(self, nombre: str, id_usuario: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT * FROM dispositivos 
                    WHERE nombre = %s AND id_usuario = %s
                """
                cursor.execute(query, (nombre, id_usuario))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar dispositivo por nombre: {error}")


    def buscar_todos(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT * FROM dispositivos
                """
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al listar dispositivos: {error}")


    def actualizar(self, dispositivo: Dispositivo):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE dispositivos 
                    SET nombre=%s, marca=%s, modelo=%s, consumo_energetico=%s
                    WHERE id_dispositivo=%s
                """
                valores = (
                    dispositivo.get_nombre(),
                    dispositivo.get_marca(),
                    dispositivo.get_modelo(),
                    dispositivo.get_consumo_energetico(),
                    dispositivo.get_id_dispositivo()
                )
                cursor.execute(query, valores)
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                raise Exception(f"Error al actualizar dispositivo: {error}")


    def eliminar(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "DELETE FROM dispositivos WHERE id_dispositivo = %s"
                cursor.execute(query, (id_dispositivo,))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                raise Exception(f"Error al eliminar dispositivo: {error}")
