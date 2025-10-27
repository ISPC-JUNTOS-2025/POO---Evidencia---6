"""
Script para verificar todos los dispositivos en la base de datos
y detectar posibles duplicados
"""
from conn.db_conn import DBConn
import mysql.connector

def verificar_dispositivos():
    with DBConn() as conn:
        try:
            cursor = conn.cursor()
            
            # Obtener todos los dispositivos con sus detalles
            query = """
                SELECT d.id_dispositivo, d.nombre, d.marca, d.modelo, d.tipo_dispositivo, d.id_usuario,
                       CONCAT(u.nombre, ' ', u.apellido) as nombre_usuario
                FROM dispositivos d
                LEFT JOIN usuarios u ON d.id_usuario = u.id_usuario
                ORDER BY d.nombre, d.id_dispositivo
            """
            cursor.execute(query)
            dispositivos = cursor.fetchall()
            
            print("\n=== Todos los dispositivos en la base de datos ===\n")
            for disp in dispositivos:
                print(f"ID: {disp[0]} | Nombre: {disp[1]} | Tipo: {disp[4]} | Usuario: {disp[6]}")
            
            print(f"\nTotal de dispositivos: {len(dispositivos)}")
            
            # Verificar si hay IDs duplicados o nombres duplicados para el mismo usuario
            print("\n--- Verificando duplicados ---")
            
            # Por nombre y usuario
            query_dup1 = """
                SELECT nombre, id_usuario, COUNT(*) as cantidad
                FROM dispositivos
                GROUP BY nombre, id_usuario
                HAVING COUNT(*) > 1
            """
            cursor.execute(query_dup1)
            duplicados_nombre = cursor.fetchall()
            
            if duplicados_nombre:
                print("\nDuplicados por nombre y usuario:")
                for dup in duplicados_nombre:
                    print(f"  Nombre: '{dup[0]}' para usuario {dup[1]} - {dup[2]} veces")
            else:
                print("[OK] No hay duplicados por nombre y usuario")
            
            # Por ID (esto no debería pasar nunca)
            query_dup2 = """
                SELECT id_dispositivo, COUNT(*) as cantidad
                FROM dispositivos
                GROUP BY id_dispositivo
                HAVING COUNT(*) > 1
            """
            cursor.execute(query_dup2)
            duplicados_id = cursor.fetchall()
            
            if duplicados_id:
                print("\n⚠ ERROR CRÍTICO: IDs duplicados encontrados:")
                for dup in duplicados_id:
                    print(f"  ID: {dup[0]} - {dup[1]} veces")
            else:
                print("[OK] No hay IDs duplicados")
                
        except mysql.connector.Error as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    verificar_dispositivos()
