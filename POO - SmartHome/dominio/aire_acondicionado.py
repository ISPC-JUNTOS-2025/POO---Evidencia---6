from datetime import datetime
from enums.tipodispositivo import TipoDispositivo
from dominio.dispositivo import Dispositivo


class AireAcondicionado(Dispositivo):
    def __init__(self, nombre: str = None, marca: str = None, modelo: str = None,
                 consumo_energetico: float = None, temperatura_objetivo: int = 24,
                 modo_eco: bool = False, fecha_creacion: datetime = None, id_usuario=None):
        super().__init__(nombre, marca, modelo, consumo_energetico, id_usuario)
        self._tipo_dispositivo = TipoDispositivo.ELECTRODOMESTICO
        self._fecha_creacion = datetime.now()
        self.__temperatura_objetivo = temperatura_objetivo
        self.__modo_eco = modo_eco

    def get_temperatura_objetivo(self) -> int:
        return self.__temperatura_objetivo

    def set_temperatura_objetivo(self, valor: int):
        self.__temperatura_objetivo = valor

    def get_modo_eco(self) -> bool:
        return self.__modo_eco

    def set_modo_eco(self, valor: bool):
        self.__modo_eco = valor
    
    def get_temperatura_actual(self) -> int:
        return self.__temperatura_objetivo
    
    def get_modo(self) -> bool:
        return self.__modo_eco


    def encender(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede encender el aire '{self.get_nombre()}' porque está eliminado.")
        if self.get_activado():
            raise ValueError(f"El aire '{self.get_nombre()}' ya está encendido.")

        self.set_activado(True)
        return f"Aire acondicionado '{self.get_nombre()}' encendido correctamente."

    def apagar(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede apagar el aire '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise ValueError(f"El aire '{self.get_nombre()}' ya está apagado.")

        self.set_activado(False)
        return f"Aire acondicionado '{self.get_nombre()}' apagado correctamente."

    def crear_dispositivo(self, nombre: str, marca: str, modelo: str,
                          consumo_energetico: float, id_usuario: int = None,
                          temperatura_objetivo: int = 0, modo_eco: bool = False):

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
        self.set_temperatura_objetivo(temperatura_objetivo)
        self.set_modo_eco(modo_eco)
        self.set_id_usuario(id_usuario)

        return self

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
        return f"Aire acondicionado '{nombre}' marcado como eliminado."

    def establecer_temperatura(self, nueva_temperatura: int):
        if self._eliminado:
            raise RuntimeError(f"No se puede ajustar la temperatura del aire '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede ajustar la temperatura porque el aire '{self.get_nombre()}' está apagado.")
        if not isinstance(nueva_temperatura, int):
            raise TypeError("La temperatura debe ser un número entero.")
        if not 16 <= nueva_temperatura <= 30:
            raise ValueError("La temperatura debe estar entre 16°C y 30°C.")

        self.set_temperatura_objetivo(nueva_temperatura)
        return f"Temperatura del aire '{self.get_nombre()}' ajustada a {self.get_temperatura_objetivo()}°C."

    def activar_modo_eco(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede activar modo eco del aire '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede activar modo eco porque el aire '{self.get_nombre()}' está apagado.")
        if self.get_modo_eco():
            raise ValueError(f"El modo eco del aire '{self.get_nombre()}' ya está activado.")

        self.set_modo_eco(True)
        return f"Modo eco del aire '{self.get_nombre()}' activado correctamente."

    def desactivar_modo_eco(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede desactivar modo eco del aire '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede desactivar modo eco porque el aire '{self.get_nombre()}' está apagado.")
        if not self.get_modo_eco():
            raise ValueError(f"El modo eco del aire '{self.get_nombre()}' ya está desactivado.")

        self.set_modo_eco(False)
        return f"Modo eco del aire '{self.get_nombre()}' desactivado correctamente."

    def buscar_dispositivo_por_nombre(self, nombre):
        return self.buscar_por_nombre(nombre)
    
    def eliminar_dispositivo_por_nombre(self, nombre):
        return self.eliminar_por_nombre(nombre)

    def __str__(self):
        estado = "Encendido" if self.get_activado() else "Apagado"
        modo = "Activado" if self.get_modo_eco() else "Desactivado"
        return (f"AireAcondicionado(nombre={self.get_nombre()}, marca={self.get_marca()}, "
                f"modelo={self.get_modelo()}, estado={estado}, temperatura={self.get_temperatura_objetivo()}°C, "
                f"modo_eco={modo}, consumo={self.get_consumo_energetico()}, usuario_id={self.get_id_usuario()})")