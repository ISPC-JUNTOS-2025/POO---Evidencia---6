from dao.interfaces.i_aire_acondicionado_dao import IAireAcondicionadoDAO
from dominio.aire_acondicionado import AireAcondicionado
from conn.db_conn import DBConn
import mysql.connector


class AireAcondicionadoDAO(IAireAcondicionadoDAO):
    
    def crear(self, aire_acondicionado: AireAcondicionado):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_general = """
                    INSERT INTO dispositivos (nombre, marca, modelo, consumo_energetico, tipo_dispositivo, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                datos_generales = (
                    aire_acondicionado.get_nombre(),
                    aire_acondicionado.get_marca(),
                    aire_acondicionado.get_modelo(),
                    aire_acondicionado.get_consumo_energetico(),
                    aire_acondicionado.get_tipo_dispositivo().value,
                    aire_acondicionado.get_id_usuario()
                )
                cursor.execute(query_general, datos_generales)
                id_dispositivo = cursor.lastrowid

                query_especifica = """
                    INSERT INTO aire_acondicionado (id_dispositivo, temperatura_objetivo, modo_eco)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_especifica, (
                    id_dispositivo,
                    aire_acondicionado.get_temperatura_objetivo(),
                    aire_acondicionado.get_modo_eco()
                ))
                
                conn.commit()
                return id_dispositivo
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al crear aire acondicionado: {error}")

    def buscar_por_id(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, a.temperatura_objetivo, a.modo_eco
                    FROM dispositivos d
                    INNER JOIN aire_acondicionado a ON d.id_dispositivo = a.id_dispositivo
                    WHERE d.id_dispositivo = %s
                """
                cursor.execute(query, (id_dispositivo,))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar aire acondicionado por ID: {error}")

    def buscar_por_usuario(self, id_usuario: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, a.temperatura_objetivo, a.modo_eco
                    FROM dispositivos d
                    INNER JOIN aire_acondicionado a ON d.id_dispositivo = a.id_dispositivo
                    WHERE d.id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar aires acondicionados por usuario: {error}")

    def buscar_todos(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, a.temperatura_objetivo, a.modo_eco
                    FROM dispositivos d
                    INNER JOIN aire_acondicionado a ON d.id_dispositivo = a.id_dispositivo
                """
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al listar todos los aires acondicionados: {error}")

    def actualizar(self, aire_acondicionado: AireAcondicionado):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_dispositivo = """
                    UPDATE dispositivos 
                    SET nombre=%s, marca=%s, modelo=%s, consumo_energetico=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_dispositivo, (
                    aire_acondicionado.get_nombre(),
                    aire_acondicionado.get_marca(),
                    aire_acondicionado.get_modelo(),
                    aire_acondicionado.get_consumo_energetico(),
                    aire_acondicionado.get_id_dispositivo()
                ))
                
                query_aire = """
                    UPDATE aire_acondicionado 
                    SET temperatura_objetivo=%s, modo_eco=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_aire, (
                    aire_acondicionado.get_temperatura_objetivo(),
                    aire_acondicionado.get_modo_eco(),
                    aire_acondicionado.get_id_dispositivo()
                ))
                
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar aire acondicionado: {error}")

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
                raise Exception(f"Error al eliminar aire acondicionado: {error}")

    def actualizar_temperatura(self, id_dispositivo: int, temperatura: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE aire_acondicionado SET temperatura_objetivo = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (temperatura, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar temperatura: {error}")

    def actualizar_modo_eco(self, id_dispositivo: int, modo_eco: bool):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE aire_acondicionado SET modo_eco = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (modo_eco, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar modo eco: {error}")
