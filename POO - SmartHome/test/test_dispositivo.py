import pytest
from datetime import datetime
from abc import ABC
from dominio.dispositivo import Dispositivo


class DispositivoConcreto(Dispositivo):
    
    def encender(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede encender el dispositivo '{self.get_nombre()}' porque está eliminado.")
        if self.get_activado():
            raise ValueError(f"El dispositivo '{self.get_nombre()}' ya está encendido.")
        
        self.set_activado(True)
        return f"Dispositivo '{self.get_nombre()}' encendido correctamente."
    
    def apagar(self):
        if self._eliminado:
            raise RuntimeError(f"No se puede apagar el dispositivo '{self.get_nombre()}' porque está eliminado.")
        if not self.get_activado():
            raise ValueError(f"El dispositivo '{self.get_nombre()}' ya está apagado.")
        
        self.set_activado(False)
        return f"Dispositivo '{self.get_nombre()}' apagado correctamente."
    
    def crear_dispositivo(self, nombre, marca, modelo, consumo_energetico, id_usuario):
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
        
        return self
    
    def buscar_dispositivo_por_nombre(self, nombre):
        return self.buscar_por_nombre(nombre)
    
    def eliminar_dispositivo_por_nombre(self, nombre):
        return self.eliminar_por_nombre(nombre)
    
    def buscar_por_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.strip()
    
    def listar_dispositivos(self):
        return True
    
    def eliminar_por_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._eliminado = True
        return f"Dispositivo '{nombre}' marcado como eliminado."
    
    def __str__(self):
        estado = "Encendido" if self.get_activado() else "Apagado"
        return (f"DispositivoConcreto(nombre={self.get_nombre()}, marca={self.get_marca()}, "
                f"modelo={self.get_modelo()}, estado={estado}, consumo={self.get_consumo_energetico()}, "
                f"usuario_id={self.get_id_usuario()})")


class TestDispositivo:

    def test_dispositivo_es_clase_abstracta(self):
        assert issubclass(Dispositivo, ABC)
        assert hasattr(Dispositivo, '__abstractmethods__')
        assert 'encender' in Dispositivo.__abstractmethods__
        assert 'apagar' in Dispositivo.__abstractmethods__
        assert 'crear_dispositivo' in Dispositivo.__abstractmethods__
        assert 'buscar_dispositivo_por_nombre' in Dispositivo.__abstractmethods__
        assert 'listar_dispositivos' in Dispositivo.__abstractmethods__
        assert 'eliminar_dispositivo_por_nombre' in Dispositivo.__abstractmethods__
        assert '__str__' in Dispositivo.__abstractmethods__

    def test_dispositivo_creacion_basica(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        assert dispositivo.get_nombre() == "Test Device"
        assert dispositivo.get_marca() == "Test Brand"
        assert dispositivo.get_modelo() == "Test Model"
        assert dispositivo.get_consumo_energetico() == 100.5
        assert dispositivo.get_id_usuario() == 1
        assert dispositivo.get_activado() is False
        assert isinstance(dispositivo.get_fecha_creacion(), datetime)
        assert dispositivo.get_tipo_dispositivo() is None

    def test_dispositivo_setters_y_getters(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        dispositivo.set_nombre("New Name")
        dispositivo.set_marca("New Brand")
        dispositivo.set_modelo("New Model")
        dispositivo.set_consumo_energetico(200.0)
        dispositivo.set_id_usuario(2)
        dispositivo.set_activado(True)
        
        assert dispositivo.get_nombre() == "New Name"
        assert dispositivo.get_marca() == "New Brand"
        assert dispositivo.get_modelo() == "New Model"
        assert dispositivo.get_consumo_energetico() == 200.0
        assert dispositivo.get_id_usuario() == 2
        assert dispositivo.get_activado() is True

    def test_dispositivo_set_nombre_trim_espacios(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.set_nombre("  New Name  ")
        assert dispositivo.get_nombre() == "New Name"

    def test_dispositivo_set_marca_trim_espacios(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.set_marca("  New Brand  ")
        assert dispositivo.get_marca() == "New Brand"

    def test_dispositivo_set_modelo_trim_espacios(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.set_modelo("  New Model  ")
        assert dispositivo.get_modelo() == "New Model"

    def test_dispositivo_encender_exitoso(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        assert dispositivo.get_activado() is False
        
        resultado = dispositivo.encender()
        
        assert "encendido correctamente" in resultado
        assert dispositivo.get_activado() is True

    def test_dispositivo_encender_ya_encendido(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.encender()
        assert dispositivo.get_activado() is True
        
        with pytest.raises(ValueError, match="ya está encendido"):
            dispositivo.encender()

    def test_dispositivo_apagar_exitoso(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.encender()
        assert dispositivo.get_activado() is True
        
        resultado = dispositivo.apagar()
        
        assert "apagado correctamente" in resultado
        assert dispositivo.get_activado() is False

    def test_dispositivo_apagar_ya_apagado(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        assert dispositivo.get_activado() is False
        
        with pytest.raises(ValueError, match="ya está apagado"):
            dispositivo.apagar()

    def test_dispositivo_encender_eliminado(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            dispositivo.encender()

    def test_dispositivo_apagar_eliminado(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            dispositivo.apagar()

    def test_dispositivo_crear_dispositivo_exitoso(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        resultado = dispositivo.crear_dispositivo("New Device", "New Brand", "New Model", 150.0, 1)
        
        assert resultado == dispositivo
        assert dispositivo.get_nombre() == "New Device"
        assert dispositivo.get_marca() == "New Brand"
        assert dispositivo.get_modelo() == "New Model"
        assert dispositivo.get_consumo_energetico() == 150.0
        assert dispositivo.get_id_usuario() == 1

    def test_dispositivo_crear_dispositivo_nombre_vacio(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        with pytest.raises(ValueError, match="El nombre del dispositivo no puede estar vacío"):
            dispositivo.crear_dispositivo("", "Brand", "Model", 100.0, 1)

    def test_dispositivo_crear_dispositivo_consumo_cero(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        with pytest.raises(ValueError, match="El consumo energético debe ser mayor que cero"):
            dispositivo.crear_dispositivo("Device", "Brand", "Model", 0, 1)

    def test_dispositivo_crear_dispositivo_consumo_negativo(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        with pytest.raises(ValueError, match="El consumo energético debe ser mayor que cero"):
            dispositivo.crear_dispositivo("Device", "Brand", "Model", -50.0, 1)

    def test_dispositivo_crear_dispositivo_marca_vacia(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        with pytest.raises(ValueError, match="La marca y el modelo son obligatorios"):
            dispositivo.crear_dispositivo("Device", "", "Model", 100.0, 1)

    def test_dispositivo_crear_dispositivo_modelo_vacio(self):
        dispositivo = DispositivoConcreto(None, None, None, None, None)
        
        with pytest.raises(ValueError, match="La marca y el modelo son obligatorios"):
            dispositivo.crear_dispositivo("Device", "Brand", "", 100.0, 1)

    def test_dispositivo_buscar_por_nombre_exitoso(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        resultado = dispositivo.buscar_por_nombre("Test Device")
        
        assert resultado == "Test Device"

    def test_dispositivo_buscar_por_nombre_vacio(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            dispositivo.buscar_por_nombre("")

    def test_dispositivo_eliminar_por_nombre_exitoso(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        resultado = dispositivo.eliminar_por_nombre("Test Device")
        
        assert "marcado como eliminado" in resultado
        assert dispositivo._eliminado is True

    def test_dispositivo_eliminar_por_nombre_vacio(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            dispositivo.eliminar_por_nombre("")

    def test_dispositivo_str_representacion(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        
        resultado = str(dispositivo)
        
        assert "Test Device" in resultado
        assert "Test Brand" in resultado
        assert "Test Model" in resultado
        assert "Apagado" in resultado
        assert "100.5" in resultado
        assert "usuario_id=1" in resultado

    def test_dispositivo_str_representacion_encendido(self):
        dispositivo = DispositivoConcreto("Test Device", "Test Brand", "Test Model", 100.5, 1)
        dispositivo.encender()
        
        resultado = str(dispositivo)
        
        assert "Encendido" in resultado
