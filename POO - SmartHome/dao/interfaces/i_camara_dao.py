from abc import ABC, abstractmethod
from dominio.camara import Camara

class ICamaraDAO(ABC):

    @abstractmethod
    def crear(self, camara: Camara):
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
    def actualizar(self, camara: Camara):
        pass

    @abstractmethod
    def eliminar(self, id_dispositivo: int):
        pass

    @abstractmethod
    def actualizar_resolucion(self, id_dispositivo: int, resolucion: str):
        pass

    @abstractmethod
    def actualizar_vision_nocturna(self, id_dispositivo: int, vision_nocturna: bool):
        pass

    @abstractmethod
    def actualizar_grabacion(self, id_dispositivo: int, grabacion: bool):
        pass
