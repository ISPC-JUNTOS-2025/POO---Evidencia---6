"""
Script para limpiar dispositivos duplicados en la base de datos.
Este script elimina los registros duplicados manteniendo solo el primero.
"""
from conn.db_conn import DBConn
import mysql.connector

def limpiar_duplicados():
    with DBConn() as conn:
        try:
            cursor = conn.cursor()
            
            # Mostrar los duplicados antes de eliminar
            query_ver = """
                SELECT nombre, id_usuario, COUNT(*) as cantidad
                FROM dispositivos
                GROUP BY nombre, id_usuario
                HAVING COUNT(*) > 1
            """
            cursor.execute(query_ver)
            duplicados = cursor.fetchall()
            
            if not duplicados:
                print("No se encontraron dispositivos duplicados.")
                return
            
            print("\n--- Dispositivos duplicados encontrados ---")
            for dup in duplicados:
                print(f"Nombre: {dup[0]}, Usuario ID: {dup[1]}, Cantidad: {dup[2]}")
            
            confirmacion = input("\n¿Desea eliminar los duplicados? (s/n): ")
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Eliminar duplicados manteniendo solo el primero
            query_eliminar = """
                DELETE d1 FROM dispositivos d1
                INNER JOIN dispositivos d2 
                WHERE d1.id_dispositivo > d2.id_dispositivo 
                AND d1.nombre = d2.nombre 
                AND d1.id_usuario = d2.id_usuario
            """
            cursor.execute(query_eliminar)
            conn.commit()
            
            eliminados = cursor.rowcount
            print(f"\n✓ Se eliminaron {eliminados} dispositivos duplicados.")
            
            # Verificar que ya no hay duplicados
            cursor.execute(query_ver)
            duplicados_restantes = cursor.fetchall()
            
            if duplicados_restantes:
                print(f"\n⚠ Aún quedan {len(duplicados_restantes)} dispositivos duplicados.")
            else:
                print("\n✓ No quedan dispositivos duplicados.")
                
        except mysql.connector.Error as error:
            print(f"Error: {error}")
            conn.rollback()

if __name__ == "__main__":
    print("=== Limpiador de Dispositivos Duplicados ===\n")
    limpiar_duplicados()
    print("\n=== Proceso completado ===")
