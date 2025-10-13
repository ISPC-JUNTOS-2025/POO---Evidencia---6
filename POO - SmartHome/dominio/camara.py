from datetime import datetime
from enums.tipodispositivo import TipoDispositivo
from dominio.dispositivo import Dispositivo



class Camara(Dispositivo):
    def __init__(self, nombre: str = None, marca: str = None, modelo: str = None,
                 consumo_energetico: float = None, resolucion: str = "1080p",
                 vision_nocturna: bool = True, almacenamiento_local: bool = True,
                 fecha_creacion: datetime = None, id_usuario=None):
        super().__init__(nombre, marca, modelo, consumo_energetico, id_usuario)
        self._tipo_dispositivo = TipoDispositivo.DISPOSITIVO_DE_GRABACION
        self._fecha_creacion = datetime.now()
        self.__resolucion = resolucion
        self.__vision_nocturna = vision_nocturna
        self.__grabacion = False
        self.__almacenamiento_local = almacenamiento_local

    def get_resolucion(self) -> str:
        return self.__resolucion

    def set_resolucion(self, valor: str):
        self.__resolucion = valor

    def get_vision_nocturna(self) -> bool:
        return self.__vision_nocturna

    def set_vision_nocturna(self, valor: bool):
        self.__vision_nocturna = valor

    def get_grabacion(self) -> bool:
        return self.__grabacion

    def set_grabacion(self, valor: bool):
        self.__grabacion = valor

    def get_almacenamiento_local(self) -> bool:
        return self.__almacenamiento_local

    def set_almacenamiento_local(self, valor: bool):
        self.__almacenamiento_local = valor


    def encender(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede encender la cámara '{self.get_nombre()}' porque está eliminada.")
        if self.get_activado():
            raise ValueError(f"La cámara '{self.get_nombre()}' ya está encendida.")

        self.set_activado(True)
        return f"Cámara '{self.get_nombre()}' encendida correctamente - Resolución: {self.get_resolucion()}."

    def apagar(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede apagar la cámara '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise ValueError(f"La cámara '{self.get_nombre()}' ya está apagada.")

        if self.get_grabacion():
            self.detener_grabacion()

        self.set_activado(False)
        return f"Cámara '{self.get_nombre()}' apagada correctamente."

    def crear_dispositivo(self, nombre: str, marca: str, modelo: str,
                          consumo_energetico: float, id_usuario: int = None,
                          resolucion: str = "1080p", vision_nocturna: bool = True, 
                          almacenamiento_local: bool = True):

        if not nombre or not nombre.strip():
            raise ValueError("El nombre del dispositivo no puede estar vacío.")
        if consumo_energetico is None or consumo_energetico <= 0:
            raise ValueError("El consumo energético debe ser mayor que cero.")
        if not marca or not modelo:
            raise ValueError("La marca y el modelo son obligatorios.")
        if not resolucion or not resolucion.strip():
            raise ValueError("La resolución no puede estar vacía.")

        resoluciones_validas = ["720p", "1080p", "2K", "4K"]
        if resolucion not in resoluciones_validas:
            raise ValueError(f"La resolución debe ser una de: {', '.join(resoluciones_validas)}.")

        self.set_nombre(nombre.strip())
        self.set_marca(marca.strip())
        self.set_modelo(modelo.strip())
        self.set_consumo_energetico(consumo_energetico)
        self.set_resolucion(resolucion)
        self.set_vision_nocturna(vision_nocturna)
        self.set_almacenamiento_local(almacenamiento_local)
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
        
        if self.get_grabacion():
            self.detener_grabacion()
        
        self._eliminado = True
        return f"Cámara '{nombre}' marcada como eliminada."

    def iniciar_grabacion(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede grabar con la cámara '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede iniciar grabación porque la cámara '{self.get_nombre()}' está apagada.")
        if self.get_grabacion():
            raise ValueError(f"La cámara '{self.get_nombre()}' ya está grabando.")

        self.set_grabacion(True)
        return f"Cámara '{self.get_nombre()}' iniciando grabación en {self.get_resolucion()}."

    def detener_grabacion(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede detener grabación de la cámara '{self.get_nombre()}' porque está eliminada.")
        if not self.get_grabacion():
            raise ValueError(f"La cámara '{self.get_nombre()}' no está grabando.")

        self.set_grabacion(False)
        destino = "almacenamiento local" if self.get_almacenamiento_local() else "nube"
        return f"Cámara '{self.get_nombre()}' deteniendo grabación. Video guardado en {destino}."

    def cambiar_resolucion(self, nueva_resolucion: str):
        if self._eliminado:
            raise RuntimeError(f"No se puede cambiar resolución de la cámara '{self.get_nombre()}' porque está eliminada.")
        if self.get_grabacion():
            raise RuntimeError(f"No se puede cambiar la resolución mientras la cámara '{self.get_nombre()}' está grabando.")
        
        resoluciones_validas = ["720p", "1080p", "2K", "4K"]
        if nueva_resolucion not in resoluciones_validas:
            raise ValueError(f"La resolución debe ser una de: {', '.join(resoluciones_validas)}.")

        self.set_resolucion(nueva_resolucion)
        return f"Resolución de la cámara '{self.get_nombre()}' cambiada a {self.get_resolucion()}."

    def activar_vision_nocturna(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede activar visión nocturna de la cámara '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede activar visión nocturna porque la cámara '{self.get_nombre()}' está apagada.")
        if self.get_vision_nocturna():
            raise ValueError(f"La visión nocturna de la cámara '{self.get_nombre()}' ya está activada.")

        self.set_vision_nocturna(True)
        return f"Visión nocturna de la cámara '{self.get_nombre()}' activada correctamente."

    def desactivar_vision_nocturna(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede desactivar visión nocturna de la cámara '{self.get_nombre()}' porque está eliminada.")
        if not self.get_activado():
            raise RuntimeError(f"No se puede desactivar visión nocturna porque la cámara '{self.get_nombre()}' está apagada.")
        if not self.get_vision_nocturna():
            raise ValueError(f"La visión nocturna de la cámara '{self.get_nombre()}' ya está desactivada.")

        self.set_vision_nocturna(False)
        return f"Visión nocturna de la cámara '{self.get_nombre()}' desactivada correctamente."

    def buscar_dispositivo_por_nombre(self, nombre):
        return self.buscar_por_nombre(nombre)
    
    def eliminar_dispositivo_por_nombre(self, nombre):
        return self.eliminar_por_nombre(nombre)

    def __str__(self):
        estado = "Encendida" if self.get_activado() else "Apagada"
        grabando = "Grabando" if self.get_grabacion() else "En espera"
        vision = "Activada" if self.get_vision_nocturna() else "Desactivada"
        almacenamiento = "Local" if self.get_almacenamiento_local() else "Nube"
        
        return (f"Camara(nombre={self.get_nombre()}, marca={self.get_marca()}, modelo={self.get_modelo()}, "
                f"estado={estado}, grabacion={grabando}, resolucion={self.get_resolucion()}, "
                f"vision_nocturna={vision}, almacenamiento={almacenamiento}, "
                f"consumo={self.get_consumo_energetico()}, usuario_id={self.get_id_usuario()})")