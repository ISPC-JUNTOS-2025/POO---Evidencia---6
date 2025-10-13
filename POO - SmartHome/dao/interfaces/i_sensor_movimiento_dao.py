from abc import ABC, abstractmethod
from dominio.SensorMovimiento import SensorMovimiento

class ISensorMovimientoDAO(ABC):

    @abstractmethod
    def crear(self, sensor: SensorMovimiento):
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
    def actualizar(self, sensor: SensorMovimiento):
        pass

    @abstractmethod
    def eliminar(self, id_dispositivo: int):
        pass

    @abstractmethod
    def actualizar_estado_activo(self, id_dispositivo: int, estado_activo: bool):
        pass

    @abstractmethod
    def registrar_deteccion(self, id_dispositivo: int, fecha_deteccion):
        pass

    @abstractmethod
    def buscar_detecciones_por_sensor(self, id_dispositivo: int):
        pass
