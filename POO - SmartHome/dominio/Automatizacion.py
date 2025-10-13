from typing import List, Any
from datetime import datetime

class Automatizacion:
    
    def __init__(self, id_automatizacion: int = None, nombre: str = None, descripcion: str = None, 
                 regla: str = None, condicion: str = None, accion: str = None, id_usuario: int = None):
        self._id_automatizacion = id_automatizacion
        self._nombre = nombre
        self._descripcion = descripcion
        self._estado = False
        self._regla = regla
        self._condicion = condicion
        self._accion = accion
        self._id_usuario = id_usuario
        self._dispositivos_controlados = []
        self._fecha_creacion = datetime.now()
    
    def get_id_automatizacion(self) -> int:
        return self._id_automatizacion
    
    def get_nombre(self) -> str:
        return self._nombre
    
    def set_nombre(self, valor: str) -> None:
        self._nombre = valor
    
    def get_descripcion(self) -> str:
        return self._descripcion
    
    def set_descripcion(self, valor: str) -> None:
        self._descripcion = valor
    
    def get_estado(self) -> bool:
        return self._estado
    
    def set_estado(self, valor: bool) -> None:
        self._estado = valor
    
    def get_regla(self) -> str:
        return self._regla
    
    def set_regla(self, valor: str) -> None:
        self._regla = valor
    
    def get_condicion(self) -> str:
        return self._condicion
    
    def set_condicion(self, valor: str) -> None:
        self._condicion = valor
    
    def get_accion(self) -> str:
        return self._accion
    
    def set_accion(self, valor: str) -> None:
        self._accion = valor
    
    def get_id_usuario(self) -> int:
        return self._id_usuario
    
    def set_id_usuario(self, valor: int) -> None:
        self._id_usuario = valor
    
    def get_dispositivos_controlados(self) -> List[Any]:
        return self._dispositivos_controlados.copy()
    
    def get_fecha_creacion(self) -> datetime:
        return self._fecha_creacion
    
    def crear_automatizacion(self, nombre: str, descripcion: str, regla: str, 
                            condicion: str, accion: str, id_usuario: int) -> 'Automatizacion':
        """Crea una nueva automatización con validaciones"""
        try:
            if not nombre or not nombre.strip():
                raise ValueError("El nombre no puede estar vacío")
            if not descripcion or not descripcion.strip():
                raise ValueError("La descripción no puede estar vacía")
            if not regla or not regla.strip():
                raise ValueError("La regla no puede estar vacía")
            if not condicion or not condicion.strip():
                raise ValueError("La condición no puede estar vacía")
            if not accion or not accion.strip():
                raise ValueError("La acción no puede estar vacía")
            if not id_usuario or id_usuario <= 0:
                raise ValueError("El ID de usuario debe ser válido")
            
            self.set_nombre(nombre.strip())
            self.set_descripcion(descripcion.strip())
            self.set_regla(regla.strip())
            self.set_condicion(condicion.strip())
            self.set_accion(accion.strip())
            self.set_id_usuario(id_usuario)
            
            return self
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al crear automatización: {error}")
    
    def activar_automatizacion_encender_luces(self) -> bool:
        """Activa la automatización para encender luces"""
        try:
            if not self._estado:
                self._estado = True
                
                luces = [d for d in self._dispositivos_controlados if hasattr(d, 'regular_intensidad')]
                
                if luces:
                    for luz in luces:
                        if hasattr(luz, 'encender'):
                            luz.encender()
                            if hasattr(luz, 'regular_intensidad'):
                                luz.regular_intensidad(80)
                    return True
                else:
                    raise ValueError("No hay luces configuradas en esta automatización")
            else:
                raise ValueError("La automatización ya está activa")
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al activar automatización: {error}")
    
    def desactivar_automatizacion_encender_luces(self) -> bool:
        """Desactiva la automatización para encender luces"""
        try:
            if self._estado:
                self._estado = False
                
                luces = [d for d in self._dispositivos_controlados if hasattr(d, 'regular_intensidad')]
                
                if luces:
                    for luz in luces:
                        if hasattr(luz, 'apagar'):
                            luz.apagar()
                    return True
                else:
                    raise ValueError("No hay luces configuradas en esta automatización")
            else:
                raise ValueError("La automatización ya está desactivada")
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al desactivar automatización: {error}")
    
    def consultar_automatizaciones_activas(self) -> dict:
        """Consulta información de automatizaciones activas"""
        try:
            return {
                'id_automatizacion': self._id_automatizacion,
                'nombre': self._nombre,
                'descripcion': self._descripcion,
                'estado': 'Activa' if self._estado else 'Inactiva',
                'regla': self._regla,
                'condicion': self._condicion,
                'accion': self._accion,
                'dispositivos_controlados': len(self._dispositivos_controlados)
            }
        except Exception as error:
            raise Exception(f"Error al consultar automatizaciones activas: {error}")
    
    def mostrar_informacion_automatizacion(self) -> str:
        """Muestra información detallada de la automatización"""
        try:
            info = f"\n=== INFORMACIÓN DE AUTOMATIZACIÓN ==="
            info += f"\nAutomatización: {self._nombre}"
            info += f"\nEstado: {'Activa' if self._estado else 'Inactiva'}"
            info += f"\nDescripción: {self._descripcion}"
            info += f"\nRegla: {self._regla}"
            info += f"\nCondición: {self._condicion}"
            info += f"\nAcción: {self._accion}"
            info += f"\nDispositivos controlados: {len(self._dispositivos_controlados)}"
            
            if self._dispositivos_controlados:
                info += f"\n\nDispositivos controlados:"
                for i, dispositivo in enumerate(self._dispositivos_controlados, 1):
                    tipo = getattr(dispositivo, '_tipo_dispositivo', 'Desconocido')
                    info += f"\n  {i}. {dispositivo.get_nombre()} ({tipo})"
            
            return info
        except Exception as error:
            raise Exception(f"Error al mostrar información de automatización: {error}")
    
    def agregar_dispositivo(self, dispositivo: Any) -> bool:
        """Agrega un dispositivo a la automatización"""
        try:
            if dispositivo is None:
                raise ValueError("El dispositivo no puede ser nulo")
            
            if dispositivo not in self._dispositivos_controlados:
                self._dispositivos_controlados.append(dispositivo)
                return True
            else:
                raise ValueError("El dispositivo ya está en esta automatización")
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al agregar dispositivo: {error}")
    
    def remover_dispositivo(self, dispositivo: Any) -> bool:
        """Remueve un dispositivo de la automatización"""
        try:
            if dispositivo is None:
                raise ValueError("El dispositivo no puede ser nulo")
            
            if dispositivo in self._dispositivos_controlados:
                self._dispositivos_controlados.remove(dispositivo)
                return True
            else:
                raise ValueError("El dispositivo no está en esta automatización")
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al remover dispositivo: {error}")
    
    def ejecutar_automatizacion(self) -> bool:
        """Ejecuta la automatización según su configuración"""
        try:
            if not self._estado:
                raise ValueError("La automatización está desactivada")
            
            if "encender" in self._accion.lower() and "luz" in self._accion.lower():
                return self.activar_automatizacion_encender_luces()
            elif "apagar" in self._accion.lower() and "luz" in self._accion.lower():
                return self.desactivar_automatizacion_encender_luces()
            else:
                raise ValueError("Tipo de automatización no reconocido")
        except ValueError as error:
            raise error
        except Exception as error:
            raise Exception(f"Error al ejecutar automatización: {error}")
    
    def validar_condicion(self, valor_sensor: Any = None) -> bool:
        """Valida si se cumple la condición de la automatización"""
        try:
            if "movimiento" in self._condicion.lower():
                return valor_sensor is not None and valor_sensor
            elif "hora" in self._condicion.lower():
                return True
            elif "temperatura" in self._condicion.lower():
                return True
            else:
                return True
        except Exception as error:
            raise Exception(f"Error al validar condición: {error}")
    
    def __str__(self) -> str:
        """Representación string de la automatización"""
        try:
            estado_str = "Activa" if self._estado else "Inactiva"
            return f"{self._nombre} ({estado_str}) - {self._descripcion}"
        except Exception as error:
            return f"Error al obtener representación de automatización: {error}"
