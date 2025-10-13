from abc import ABC, abstractmethod
from dominio.Luz import Luz

class ILuzDAO(ABC):

    @abstractmethod
    def crear(self, luz: Luz):
        pass

    @abstractmethod
    def buscar_por_id(self, id_dispositivo: int):
        pass

    @abstractmethod
    def buscar_por_usuario(self, id_usuario: int):
        pass

    @abstractmethod
    def buscar_todas(self):
        pass

    @abstractmethod
    def actualizar(self, luz: Luz):
        pass

    @abstractmethod
    def eliminar(self, id_dispositivo: int):
        pass

    @abstractmethod
    def actualizar_intensidad(self, id_dispositivo: int, intensidad: int):
        pass

    @abstractmethod
    def actualizar_regulable(self, id_dispositivo: int, regulable: bool):
        pass
