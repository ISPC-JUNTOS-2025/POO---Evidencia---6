from abc import ABC, abstractmethod
from datetime import datetime

class Dispositivo(ABC):
    def __init__(self, nombre: str, marca: str, modelo: str, consumo_energetico: float, id_usuario = None):
        self._id_dispositivo = None
        self._nombre = nombre
        self._marca = marca
        self._modelo = modelo
        self._activado = False
        self._consumo_energetico = consumo_energetico
        self._fecha_creacion = datetime.now()
        self._tipo_dispositivo = None
        self._id_usuario = id_usuario
    
    def get_id_dispositivo(self):
        return self._id_dispositivo
    
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, valor: str):
        self._nombre = valor.strip()
    
    def get_marca(self):
        return self._marca
    
    def set_marca(self, marca):
        self._marca = marca
    
    def get_modelo(self):
        return self._modelo
    
    def set_modelo(self, modelo):
        self._modelo = modelo
    
    def get_activado(self):
        return self._activado
    
    def set_activado(self, activado):
        self._activado = activado
    
    def get_consumo_energetico(self):
        return self._consumo_energetico
    
    def set_consumo_energetico(self, valor: float):
        self._consumo_energetico = valor
    
    def set_id_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    def get_id_usuario(self):
        return self._id_usuario 
    
    def get_tipo_dispositivo(self):
        return self._tipo_dispositivo
    
    @abstractmethod
    def encender(self): pass
    
    @abstractmethod
    def apagar(self): pass
    
    @abstractmethod
    def crear_dispositivo(self, nombre, marca, modelo, consumo_energetico, id_usuario): pass
    
    @abstractmethod
    def buscar_dispositivo_por_nombre(self, nombre): pass
    
    @abstractmethod
    def listar_dispositivos(self): pass
    
    @abstractmethod
    def eliminar_dispositivo_por_nombre(self, nombre): pass
    
    @abstractmethod
    def __str__(self): pass
