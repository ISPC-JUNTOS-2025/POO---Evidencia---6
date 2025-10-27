from abc import ABC, abstractmethod
from dominio.aire_acondicionado import AireAcondicionado

class IAireAcondicionadoDAO(ABC):

    @abstractmethod
    def crear(self, aire_acondicionado: AireAcondicionado):
        pass

    @abstractmethod
    def buscar_por_id(self, id_dispositivo: int):
        pass

    @abstractmethod
    def buscar_por_usuario(self, id_usuario: int):
        pass

    @abstractmethod
    def buscar_todos(self):
        pass

    @abstractmethod
    def actualizar(self, aire_acondicionado: AireAcondicionado):
        pass

    @abstractmethod
    def eliminar(self, id_dispositivo: int):
        pass

    @abstractmethod
    def actualizar_temperatura(self, id_dispositivo: int, temperatura: int):
        pass

    @abstractmethod
    def actualizar_modo_eco(self, id_dispositivo: int, modo_eco: bool):
        pass
