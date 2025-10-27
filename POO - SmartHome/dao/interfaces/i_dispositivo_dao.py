from abc import ABC, abstractmethod
from dominio.dispositivo import Dispositivo

class IDispositivoDAO(ABC):

    @abstractmethod
    def crear(self, dispositivo: Dispositivo):
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str, id_usuario: int):
        pass

    @abstractmethod
    def buscar_todos(self):
        pass

    @abstractmethod
    def actualizar(self, dispositivo: Dispositivo):
        pass

    @abstractmethod
    def eliminar(self, id_dispositivo: int):
        pass
    
    @abstractmethod
    def buscar_por_nombre_global(self, nombre: str):
        pass