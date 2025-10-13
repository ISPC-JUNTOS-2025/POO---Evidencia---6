from abc import ABC, abstractmethod
from dominio.usuario import Usuario

class IUsuarioDAO(ABC):

    @abstractmethod
    def crear(usuario: Usuario):
        pass

    @abstractmethod
    def buscar_usuarios():
        pass

    @abstractmethod
    def actualizar_rol_usuario(usuario: Usuario):
        pass
