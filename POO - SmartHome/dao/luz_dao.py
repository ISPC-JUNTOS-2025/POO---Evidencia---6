from dao.interfaces.i_luz_dao import ILuzDAO
from dominio.luz import Luz
from conn.db_conn import DBConn
import mysql.connector


class LuzDAO(ILuzDAO):
    
    def crear(self, luz: Luz):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query_general = """
                    INSERT INTO dispositivos (nombre, marca, modelo, consumo_energetico, tipo_dispositivo, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                datos_generales = (
                    luz.get_nombre(),
                    luz.get_marca(),
                    luz.get_modelo(),
                    luz.get_consumo_energetico(),
                    luz.get_tipo_dispositivo().value,
                    luz.get_id_usuario()
                )
                cursor.execute(query_general, datos_generales)
                id_dispositivo = cursor.lastrowid

                query_especifica = """
                    INSERT INTO luz (id_dispositivo, intensidad, regulable)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_especifica, (
                    id_dispositivo,
                    luz.get_intensidad(),
                    luz.get_regulable()
                ))
                
                conn.commit()
                return id_dispositivo
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al crear luz: {error}")

    def buscar_por_id(self, id_dispositivo: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, l.intensidad, l.regulable
                    FROM dispositivos d
                    INNER JOIN luz l ON d.id_dispositivo = l.id_dispositivo
                    WHERE d.id_dispositivo = %s
                """
                cursor.execute(query, (id_dispositivo,))
                return cursor.fetchone()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar luz por ID: {error}")

    def buscar_por_usuario(self, id_usuario: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, l.intensidad, l.regulable
                    FROM dispositivos d
                    INNER JOIN luz l ON d.id_dispositivo = l.id_dispositivo
                    WHERE d.id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar luces por usuario: {error}")

    def buscar_todas(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT d.*, l.intensidad, l.regulable
                    FROM dispositivos d
                    INNER JOIN luz l ON d.id_dispositivo = l.id_dispositivo
                """
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as error:
                raise Exception(f"Error al listar todas las luces: {error}")

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
                    luz.get_nombre(),
                    luz.get_marca(),
                    luz.get_modelo(),
                    luz.get_consumo_energetico(),
                    luz.get_id_dispositivo()
                ))
                
                query_luz = """
                    UPDATE luz 
                    SET intensidad=%s, regulable=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(query_luz, (
                    luz.get_intensidad(),
                    luz.get_regulable(),
                    luz.get_id_dispositivo()
                ))
                
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar luz: {error}")

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
                raise Exception(f"Error al eliminar luz: {error}")

    def actualizar_intensidad(self, id_dispositivo: int, intensidad: int):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE luz SET intensidad = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (intensidad, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar intensidad: {error}")

    def actualizar_regulable(self, id_dispositivo: int, regulable: bool):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE luz SET regulable = %s WHERE id_dispositivo = %s"
                cursor.execute(query, (regulable, id_dispositivo))
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                conn.rollback()
                raise Exception(f"Error al actualizar regulable: {error}")