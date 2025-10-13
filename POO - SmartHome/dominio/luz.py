from datetime import datetime
from enums.tipodispositivo import TipoDispositivo
from dominio.dispositivo import Dispositivo


class Luz(Dispositivo):
    def __init__(self, nombre: str = None, marca: str = None, modelo: str = None,
                 consumo_energetico: float = None,
                 intensidad: int = 100, regulable: bool = False, fecha_creacion: datetime = None, id_usuario = None):
        super().__init__(nombre, marca, modelo, consumo_energetico, id_usuario)
        self._tipo_dispositivo = TipoDispositivo.LUZ
        self._fecha_creacion = datetime.now()
        self.__intensidad = intensidad
        self.__regulable = regulable

    def get_intensidad(self) -> int:
        return self.__intensidad

    def set_intensidad(self, valor: int):
        self.__intensidad = valor

    def get_regulable(self) -> bool:
        return self.__regulable

    def set_regulable(self, valor: bool):
        self.__regulable = valor


    def encender(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede encender la luz '{self.get_nombre()}' porque está eliminada.")
        if self.get_activado():
            raise ValueError(f"La luz '{self.get_nombre()}' ya está encendida.")

        self.set_activado(True)
        return f"Luz '{self.get_nombre()}' encendida correctamente."

    def apagar(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede apagar la luz '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise ValueError(f"La luz '{self.get_nombre()}' ya está apagada.")

        self.set_activado(False)
        return f"Luz '{self.get_nombre()}' apagada correctamente."

    def crear_dispositivo(self, nombre: str, marca: str, modelo: str,
                          consumo_energetico: float, id_usuario: int = None,
                          intensidad: int = 100, regulable: bool = False):

        if not nombre or not nombre.strip():
            raise ValueError("El nombre del dispositivo no puede estar vacío.")
        if consumo_energetico is None or consumo_energetico <= 0:
            raise ValueError("El consumo energético debe ser mayor que cero.")
        if not marca or not modelo:
            raise ValueError("La marca y el modelo son obligatorios.")

        self.set_nombre(nombre.strip())
        self.set_marca(marca.strip())
        self.set_modelo(modelo.strip())
        self.set_consumo_energetico(consumo_energetico)
        self.set_regulable(regulable)
        self.set_intensidad(intensidad)
        self.set_id_usuario(id_usuario)

        return self

    def regular_intensidad(self, nueva_intensidad: int):
        if self._eliminado:
            raise RuntimeError(f"No se puede regular la luz '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede regular la intensidad porque la luz '{self.get_nombre()}' está apagada.")
        if not self.get_regulable():
            raise ValueError(f"La luz '{self.get_nombre()}' no es regulable.")
        if not isinstance(nueva_intensidad, int):
            raise TypeError("La intensidad debe ser un número entero.")
        if not 0 <= nueva_intensidad <= 100:
            raise ValueError("La intensidad debe estar entre 0 y 100.")

        self.set_intensidad(nueva_intensidad)
        return f"Intensidad de la luz '{self.get_nombre()}' ajustada a {self.get_intensidad()}%."

    def buscar_por_nombre(self, nombre: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.strip()

    def listar_dispositivos(self):
        return True 

    def eliminar_por_nombre(self, nombre: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._eliminado = True
        return f"Luz '{nombre}' marcada como eliminada."

    def buscar_dispositivo_por_nombre(self, nombre):
        return self.buscar_por_nombre(nombre)
    
    def eliminar_dispositivo_por_nombre(self, nombre):
        return self.eliminar_por_nombre(nombre)

    def __str__(self):
        estado = "Encendida" if self.get_activado() else "Apagada"
        return (f"Luz(nombre={self.get_nombre()}, marca={self.get_marca()}, modelo={self.get_modelo()}, "
                f"estado={estado}, intensidad={self.get_intensidad()}, regulable={self.get_regulable()}, "
                f"consumo={self.get_consumo_energetico()}, usuario_id={self.get_id_usuario()})")
