from datetime import datetime
from enums.Rol import Rol
from utilidades.utilidades import verificar_email, encriptar_contraseña

class Usuario:
    def __init__(self):
        self.__id_usuario = None
        self.__nombre = None
        self.__apellido = None
        self.__email = None
        self.__contraseña = None
        self.__rol = None
        self.__calle = None
        self.__numero = None
        self.__fecha_creacion = None
        self.__esta_eliminado = False
        self.__dispositivos = []

        
    def get_id_usuario(self):
        return self.__id_usuario
    
    def set_id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario
        
    def get_nombre(self):
        return self.__nombre
    
    def set_nombre(self, nombre):
        self.__nombre = nombre.strip()
    
    def get_apellido(self):
        return self.__apellido
    
    def set_apellido(self, apellido):
        self.__apellido = apellido.strip()
    
    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email

    def get_contraseña(self):
        return self.__contraseña

    def set_contraseña(self, contraseña):
        self.__contraseña = contraseña.strip()
    
    def get_rol(self):
        return self.__rol

    def set_rol(self, rol: Rol):
        self.__rol = rol

    def set_calle(self, calle):
        self.__calle = calle

    def get_calle(self):
        return self.__calle

    def set_numero(self, numero):
        self.__numero = numero

    def get_numero(self):
        return self.__numero
    
    def get_fecha_creacion(self):
        return self.__fecha_creacion
    
    def get_dispositivos(self):
        return self.__dispositivos.copy()
    
    def agregar_dispositivo(self, dispositivo):
        if dispositivo not in self.__dispositivos:
            self.__dispositivos.append(dispositivo)
            dispositivo.set_id_usuario(self.__id_usuario)
    
    def remover_dispositivo(self, dispositivo):
        if dispositivo in self.__dispositivos:
            self.__dispositivos.remove(dispositivo)

    def registrar_usuario(self, nombre, apellido, email, contraseña, calle, numero):
        try:
            if not nombre or not nombre.strip():
                raise ValueError("El nombre no puede estar vacío")
            
            if not apellido or not apellido.strip():
                raise ValueError("El apellido no puede estar vacío")
            
            if not contraseña or not contraseña.strip():
                raise ValueError("La contraseña no puede estar vacía")
            
            if len(contraseña.strip()) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            
            if not calle or not calle.strip():
                raise ValueError("La calle no puede estar vacía")

            if not numero:
                raise ValueError("El número no puede estar vacío")
            
            verificar_email(email)

            self.__nombre = nombre.strip()
            self.__apellido = apellido.strip()
            self.__email = email.strip().lower()
            self.__contraseña = encriptar_contraseña(contraseña.strip())
            self.__calle = calle.strip()
            self.__numero = numero
            self.__rol = Rol.USUARIO
            self.__fecha_creacion = datetime.now()
            
            return self
        
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al registrar usuario: {error}")


    def iniciar_sesion(self, email: str, contraseña: str):
        try:
            if not email or not email.strip():
                raise ValueError("El email no puede estar vacío")
            
            if not contraseña or not contraseña.strip():
                raise ValueError("La contraseña no puede estar vacía")
            
            verificar_email(email)
            
            if self.get_email() != email.strip().lower():
                raise ValueError("Email o contraseña incorrectos")
            
            contraseña_encriptada = encriptar_contraseña(contraseña.strip())
            
            if self.__contraseña != contraseña_encriptada:
                raise ValueError("Email o contraseña incorrectos")
            
            return {
                'nombre': self.get_nombre(),
                'apellido': self.get_apellido(),
                'email': self.get_email()
            }
            
        except ValueError as error:
            raise error
        except Exception as e:
            raise Exception(f"Error al iniciar sesión: {e}")

    def consultar_datos_personales(self):
        try:
            return {
                'nombre': self.get_nombre(),
                'apellido': self.get_apellido(),
                'email': self.get_email(),
                'calle': self.get_calle(),
                'numero': self.get_numero(),
                'rol': self.get_rol().value,
            }
        except Exception as e:
            raise Exception(f"Error al consultar datos personales: {e}")

    def cambiar_rol_de_usuario(self, nuevo_rol: Rol):
        try:
            if nuevo_rol is None:
                raise ValueError("El nuevo rol no puede ser nulo")
            
            if not isinstance(nuevo_rol, Rol):
                raise ValueError("El rol debe ser una instancia válida de Rol")
            
            self.set_rol(nuevo_rol)
            
            return {
                'mensaje': f"Rol actualizado exitosamente",
                'usuario': self.get_nombre(),
                'nuevo_rol': nuevo_rol.value
            }
            
        except ValueError as error:
            raise error
        except Exception as e:
            raise Exception(f"Error al cambiar rol: {e}")

    def __str__(self):
        try:
            estado = "Activo" if "Inactivo" else self.get_esta_eliminado()
            return f"{self.get_nombre()} {self.get_apellido()} - {self.get_email()} ({self.get_rol().value}) [{estado}]"
        except Exception as e:
            return f"Error al obtener representación del usuario: {e}"

