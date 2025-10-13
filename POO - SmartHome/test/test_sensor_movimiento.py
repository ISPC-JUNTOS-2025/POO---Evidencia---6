import pytest
from datetime import datetime
from dominio.sensor_movimiento import SensorMovimiento
from enums.tipodispositivo import TipoDispositivo


class TestSensorMovimiento:

    def test_sensor_movimiento_creacion_basica(self):
        sensor = SensorMovimiento()
        assert sensor.get_nombre() is None
        assert sensor.get_marca() is None
        assert sensor.get_modelo() is None
        assert sensor.get_consumo_energetico() is None
        assert sensor.get_id_usuario() is None
        assert sensor.get_estado_activo() is False
        assert sensor.get_ultima_deteccion() is None
        assert sensor.get_tipo_dispositivo() == TipoDispositivo.SENSOR
        assert isinstance(sensor.get_fecha_creacion(), datetime)

    def test_sensor_movimiento_crear_dispositivo_exitoso(self):
        sensor = SensorMovimiento()
        resultado = sensor.crear_dispositivo(
            nombre="Sensor Pasillo",
            marca="Xiaomi",
            modelo="Motion Sensor",
            consumo_energetico=2.0,
            id_usuario=1
        )
        
        assert resultado == sensor
        assert sensor.get_nombre() == "Sensor Pasillo"
        assert sensor.get_marca() == "Xiaomi"
        assert sensor.get_modelo() == "Motion Sensor"
        assert sensor.get_consumo_energetico() == 2.0
        assert sensor.get_id_usuario() == 1

    def test_sensor_movimiento_setters_y_getters(self):
        sensor = SensorMovimiento()
        
        sensor.set_estado_activo(True)
        fecha_deteccion = datetime.now()
        sensor.set_ultima_deteccion(fecha_deteccion)
        
        assert sensor.get_estado_activo() is True
        assert sensor.get_ultima_deteccion() == fecha_deteccion

    def test_sensor_movimiento_encender_exitoso(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        assert sensor.get_activado() is False
        assert sensor.get_estado_activo() is False
        
        resultado = sensor.encender()
        
        assert "activado correctamente" in resultado
        assert sensor.get_activado() is True
        assert sensor.get_estado_activo() is True

    def test_sensor_movimiento_encender_ya_encendido(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        assert sensor.get_activado() is True
        
        with pytest.raises(ValueError, match="ya está encendido"):
            sensor.encender()

    def test_sensor_movimiento_apagar_exitoso(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        assert sensor.get_activado() is True
        assert sensor.get_estado_activo() is True
        
        resultado = sensor.apagar()
        
        assert "desactivado correctamente" in resultado
        assert sensor.get_activado() is False
        assert sensor.get_estado_activo() is False

    def test_sensor_movimiento_apagar_ya_apagado(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        assert sensor.get_activado() is False
        
        with pytest.raises(ValueError, match="ya está apagado"):
            sensor.apagar()

    def test_sensor_movimiento_encender_eliminado(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            sensor.encender()

    def test_sensor_movimiento_apagar_eliminado(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            sensor.apagar()

    def test_sensor_movimiento_detectar_movimiento_exitoso(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        assert sensor.get_estado_activo() is True
        
        resultado = sensor.detectar_movimiento()
        
        assert isinstance(resultado, dict)
        assert 'id_dispositivo' in resultado
        assert 'nombre_sensor' in resultado
        assert 'fecha_deteccion' in resultado
        assert 'id_usuario' in resultado
        assert resultado['nombre_sensor'] == "Sensor Test"
        assert resultado['id_usuario'] == 1
        assert isinstance(resultado['fecha_deteccion'], datetime)
        assert sensor.get_ultima_deteccion() is not None

    def test_sensor_movimiento_detectar_movimiento_apagado(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        assert sensor.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagado"):
            sensor.detectar_movimiento()

    def test_sensor_movimiento_detectar_movimiento_eliminado(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            sensor.detectar_movimiento()

    def test_sensor_movimiento_detectar_movimiento_no_activo(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        sensor.set_estado_activo(False)  # Desactivar manualmente
        
        with pytest.raises(RuntimeError, match="no está en modo activo"):
            sensor.detectar_movimiento()

    def test_sensor_movimiento_detectar_movimiento_multiple(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        
        resultado1 = sensor.detectar_movimiento()
        primera_fecha = resultado1['fecha_deteccion']
        
        import time
        time.sleep(0.01)
        resultado2 = sensor.detectar_movimiento()
        segunda_fecha = resultado2['fecha_deteccion']
        
        assert segunda_fecha > primera_fecha
        assert sensor.get_ultima_deteccion() == segunda_fecha

    def test_sensor_movimiento_buscar_por_nombre_exitoso(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        resultado = sensor.buscar_por_nombre("Sensor Pasillo")
        
        assert resultado == "Sensor Pasillo"

    def test_sensor_movimiento_buscar_por_nombre_vacio(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            sensor.buscar_por_nombre("")

    def test_sensor_movimiento_eliminar_por_nombre_exitoso(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        resultado = sensor.eliminar_por_nombre("Sensor Pasillo")
        
        assert "marcado como eliminado" in resultado
        assert sensor._eliminado is True

    def test_sensor_movimiento_eliminar_por_nombre_vacio(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            sensor.eliminar_por_nombre("")

    def test_sensor_movimiento_str_representacion(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        resultado = str(sensor)
        
        assert "Sensor Pasillo" in resultado
        assert "Xiaomi" in resultado
        assert "Motion Sensor" in resultado
        assert "Apagado" in resultado
        assert "Inactivo" in resultado
        assert "ultima_deteccion=Ninguna" in resultado
        assert "2.0" in resultado
        assert "usuario_id=1" in resultado

    def test_sensor_movimiento_str_representacion_encendido(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        
        resultado = str(sensor)
        
        assert "Encendido" in resultado
        assert "Activo" in resultado

    def test_sensor_movimiento_str_representacion_con_deteccion(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Pasillo", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        sensor.detectar_movimiento()
        
        resultado = str(sensor)
        
        assert "ultima_deteccion=" in resultado
        assert "Ninguna" not in resultado

    def test_sensor_movimiento_fixture(self, sensor_movimiento_test):
        assert sensor_movimiento_test.get_nombre() == "Sensor Pasillo"
        assert sensor_movimiento_test.get_marca() == "Xiaomi"
        assert sensor_movimiento_test.get_modelo() == "Motion Sensor"
        assert sensor_movimiento_test.get_consumo_energetico() == 2.0
        assert sensor_movimiento_test.get_id_usuario() == 1
        assert sensor_movimiento_test.get_id_dispositivo() == 4

    def test_sensor_movimiento_estado_activo_independiente(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        
        assert sensor.get_activado() is False
        assert sensor.get_estado_activo() is False
        
        sensor.encender()
        assert sensor.get_activado() is True
        assert sensor.get_estado_activo() is True
        
        sensor.set_estado_activo(False)
        assert sensor.get_activado() is True
        assert sensor.get_estado_activo() is False
        
        sensor.apagar()
        assert sensor.get_activado() is False
        assert sensor.get_estado_activo() is False

    def test_sensor_movimiento_deteccion_actualiza_fecha(self):
        sensor = SensorMovimiento()
        sensor.crear_dispositivo("Sensor Test", "Xiaomi", "Motion Sensor", 2.0, 1)
        sensor.encender()
        
        fecha_inicial = sensor.get_ultima_deteccion()
        assert fecha_inicial is None
        
        resultado = sensor.detectar_movimiento()
        fecha_deteccion = sensor.get_ultima_deteccion()
        
        assert fecha_deteccion is not None
        assert isinstance(fecha_deteccion, datetime)
        assert fecha_deteccion == resultado['fecha_deteccion']
