from datetime import datetime
from enums.tipodispositivo import TipoDispositivo
from dominio.dispositivo import Dispositivo


class SensorMovimiento(Dispositivo):
    def __init__(self, nombre: str = None, marca: str = None, modelo: str = None,
                 consumo_energetico: float = None, fecha_creacion: datetime = None, 
                 id_usuario=None):
        super().__init__(nombre, marca, modelo, consumo_energetico, id_usuario)
        self._tipo_dispositivo = TipoDispositivo.SENSOR
        self._fecha_creacion = datetime.now()
        self.__estado_activo = False
        self.__ultima_deteccion = None
        self.__sensibilidad = 50
        self.__rango = 5.0

    def get_estado_activo(self) -> bool:
        return self.__estado_activo

    def set_estado_activo(self, valor: bool):
        self.__estado_activo = valor

    def get_ultima_deteccion(self):
        return self.__ultima_deteccion

    def set_ultima_deteccion(self, valor: datetime):
        self.__ultima_deteccion = valor
    
    def get_sensibilidad(self) -> int:
        return self.__sensibilidad
    
    def set_sensibilidad(self, valor: int):
        if not 0 <= valor <= 100:
            raise ValueError("La sensibilidad debe estar entre 0 y 100.")
        self.__sensibilidad = valor
    
    def get_rango(self) -> float:
        return self.__rango
    
    def set_rango(self, valor: float):
        if valor <= 0:
            raise ValueError("El rango debe ser mayor que cero.")
        self.__rango = valor

    def encender(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede encender el sensor '{self.get_nombre()}' porque está eliminado.")
        if self.get_activado():
            raise ValueError(f"El sensor '{self.get_nombre()}' ya está encendido.")

        self.set_activado(True)
        self.set_estado_activo(True)
        return f"Sensor '{self.get_nombre()}' activado correctamente."

    def apagar(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede apagar el sensor '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise ValueError(f"El sensor '{self.get_nombre()}' ya está apagado.")

        self.set_activado(False)
        self.set_estado_activo(False)
        return f"Sensor '{self.get_nombre()}' desactivado correctamente."

    def crear_dispositivo(self, nombre: str, marca: str, modelo: str,
                          consumo_energetico: float, id_usuario: int = None,
                          sensibilidad: int = 50, rango: float = 5.0):

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
        self.set_id_usuario(id_usuario)
        self.set_sensibilidad(sensibilidad)
        self.set_rango(rango)

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
        return f"Sensor '{nombre}' marcado como eliminado."

    def detectar_movimiento(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede detectar movimiento con el sensor '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede detectar movimiento porque el sensor '{self.get_nombre()}' está apagado.")
        if not self.get_estado_activo():
            raise RuntimeError(f"El sensor '{self.get_nombre()}' no está en modo activo.")

        ahora = datetime.now()
        self.set_ultima_deteccion(ahora)
        
        return {
            'id_dispositivo': self.get_id_dispositivo(),
            'nombre_sensor': self.get_nombre(),
            'fecha_deteccion': ahora,
            'id_usuario': self.get_id_usuario()
        }

    def buscar_dispositivo_por_nombre(self, nombre):
        return self.buscar_por_nombre(nombre)
    
    def eliminar_dispositivo_por_nombre(self, nombre):
        return self.eliminar_por_nombre(nombre)

    def __str__(self):
        estado = "Encendido" if self.get_activado() else "Apagado"
        activo = "Activo" if self.get_estado_activo() else "Inactivo"
        ultima = self.get_ultima_deteccion()
        ultima_str = ultima.strftime('%d-%m-%Y %H:%M:%S') if ultima else "Ninguna"
        
        return (f"SensorMovimiento(nombre={self.get_nombre()}, marca={self.get_marca()}, "
                f"modelo={self.get_modelo()}, estado={estado}, modo={activo}, "
                f"ultima_deteccion={ultima_str}, consumo={self.get_consumo_energetico()}, "
                f"usuario_id={self.get_id_usuario()})")