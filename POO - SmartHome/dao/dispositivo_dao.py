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
                
                query_verificar = """
                    SELECT id_dispositivo FROM dispositivos 
                    WHERE nombre = %s AND id_usuario = %s
                """
                cursor.execute(query_verificar, (dispositivo.get_nombre(), dispositivo.get_id_usuario()))
                existe = cursor.fetchone()
                
                if existe:
                    raise Exception(f"Ya existe un dispositivo con el nombre '{dispositivo.get_nombre()}' para este usuario.")
                
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
                        INSERT INTO sensor_movimiento (id_dispositivo, estado_activo, ultima_deteccion)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_estado_activo(),
                        dispositivo.get_ultima_deteccion()
                    ))

                elif isinstance(dispositivo, Camara):
                    query_especifica = """
                        INSERT INTO camara (id_dispositivo, resolucion, vision_nocturna, grabacion, almacenamiento_local)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_resolucion(),
                        dispositivo.get_vision_nocturna(),
                        dispositivo.get_grabacion(),
                        dispositivo.get_almacenamiento_local()
                    ))

                elif isinstance(dispositivo, AireAcondicionado):
                    query_especifica = """
                        INSERT INTO aire_acondicionado (id_dispositivo, temperatura_objetivo, modo_eco)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query_especifica, (
                        id_dispositivo,
                        dispositivo.get_temperatura_objetivo(),
                        dispositivo.get_modo_eco()
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
                    SELECT DISTINCT d.*, CONCAT(u.nombre, ' ', u.apellido) as nombre_usuario
                    FROM dispositivos d
                    LEFT JOIN usuarios u ON d.id_usuario = u.id_usuario
                    ORDER BY d.nombre
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
    
    def buscar_por_nombre_global(self, nombre: str):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT * FROM dispositivos 
                    WHERE nombre = %s
                """
                cursor.execute(query, (nombre,))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar dispositivo por nombre: {error}")