from dao.interfaces.i_usuario_dao import IUsuarioDAO
from dominio.usuario import Usuario
from conn.db_conn import DBConn
import mysql.connector
from enums.Rol import Rol

class UsuarioDao(IUsuarioDAO):

    def crear(self, usuario: Usuario):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = """
                INSERT INTO usuarios (nombre, apellido, email, contraseña, rol, calle, numero)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    usuario.get_nombre(),
                    usuario.get_apellido(),
                    usuario.get_email(),
                    usuario.get_contraseña(),
                    usuario.get_rol().value,
                    usuario.get_calle(),
                    usuario.get_numero()
                )
                cursor.execute(query, values)
                conn.commit()
                return usuario
            except mysql.connector.Error as error:
                raise Exception(f"Error al crear usuario: {error}")


    def buscar_usuarios(self):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = """
                SELECT id_usuario, nombre, apellido, email, contraseña, rol, calle, numero
                FROM usuarios
                """
                cursor.execute(query)
                results = cursor.fetchall()

                usuarios = []
                for result in results:
                    usuario = Usuario()
                    usuario.set_id_usuario(result[0])
                    usuario.set_nombre(result[1])
                    usuario.set_apellido(result[2])
                    usuario.set_email(result[3])
                    usuario.set_contraseña(result[4])
                    
                    # Convertir string del rol al enum Rol
                    rol_str = result[5].lower()  # "administrador", "usuario", "invitado"
                    if rol_str == "administrador":
                        usuario.set_rol(Rol.ADMINISTRADOR)
                    elif rol_str == "usuario":
                        usuario.set_rol(Rol.USUARIO)
                    elif rol_str == "invitado":
                        usuario.set_rol(Rol.INVITADO)
                    else:
                        usuario.set_rol(Rol.USUARIO)  # valor por defecto
                    
                    usuario.set_calle(result[6])
                    usuario.set_numero(result[7])
                    usuarios.append(usuario)

                return usuarios
            except mysql.connector.Error as error:
                raise Exception(f"Error al buscar usuarios: {error}")

    def actualizar_rol_usuario(self, usuario: Usuario):
        with DBConn() as conn:
            try:
                cursor = conn.cursor()
                query = """
                UPDATE usuarios SET rol = %s WHERE id_usuario = %s
                """
                values = (usuario.get_rol().value, usuario.get_id_usuario())
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as error:
                raise Exception(f"Error al actualizar rol usuario: {error}")