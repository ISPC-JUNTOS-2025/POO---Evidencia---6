import pytest
from datetime import datetime
from dominio.aire_acondicionado import AireAcondicionado
from enums.tipodispositivo import TipoDispositivo


class TestAireAcondicionado:
    def test_aire_acondicionado_creacion_basica(self):
        aire = AireAcondicionado()
        assert aire.get_nombre() is None
        assert aire.get_marca() is None
        assert aire.get_modelo() is None
        assert aire.get_consumo_energetico() is None
        assert aire.get_id_usuario() is None
        assert aire.get_temperatura_objetivo() == 24
        assert aire.get_modo_eco() is False
        assert aire.get_tipo_dispositivo() == TipoDispositivo.ELECTRODOMESTICO
        assert isinstance(aire.get_fecha_creacion(), datetime)

    def test_aire_acondicionado_crear_dispositivo_exitoso(self):
        aire = AireAcondicionado()
        resultado = aire.crear_dispositivo(
            nombre="Aire Sala",
            marca="Samsung",
            modelo="AR12",
            consumo_energetico=2000.0,
            id_usuario=1,
            temperatura_objetivo=22,
            modo_eco=True
        )
        
        assert resultado == aire
        assert aire.get_nombre() == "Aire Sala"
        assert aire.get_marca() == "Samsung"
        assert aire.get_modelo() == "AR12"
        assert aire.get_consumo_energetico() == 2000.0
        assert aire.get_id_usuario() == 1
        assert aire.get_temperatura_objetivo() == 22
        assert aire.get_modo_eco() is True

    def test_aire_acondicionado_setters_y_getters(self):
        aire = AireAcondicionado()
        
        aire.set_temperatura_objetivo(20)
        aire.set_modo_eco(True)
        
        assert aire.get_temperatura_objetivo() == 20
        assert aire.get_modo_eco() is True

    def test_aire_acondicionado_encender_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        assert aire.get_activado() is False
        
        resultado = aire.encender()
        
        assert "encendido correctamente" in resultado
        assert aire.get_activado() is True

    def test_aire_acondicionado_encender_ya_encendido(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        assert aire.get_activado() is True
        
        with pytest.raises(ValueError, match="ya está encendido"):
            aire.encender()

    def test_aire_acondicionado_apagar_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        assert aire.get_activado() is True
        
        resultado = aire.apagar()
        
        assert "apagado correctamente" in resultado
        assert aire.get_activado() is False

    def test_aire_acondicionado_apagar_ya_apagado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        assert aire.get_activado() is False
        
        with pytest.raises(ValueError, match="ya está apagado"):
            aire.apagar()

    def test_aire_acondicionado_encender_eliminado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            aire.encender()

    def test_aire_acondicionado_apagar_eliminado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            aire.apagar()

    def test_aire_acondicionado_establecer_temperatura_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        resultado = aire.establecer_temperatura(20)
        
        assert "ajustada a 20°C" in resultado
        assert aire.get_temperatura_objetivo() == 20

    def test_aire_acondicionado_establecer_temperatura_apagado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        assert aire.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagado"):
            aire.establecer_temperatura(20)

    def test_aire_acondicionado_establecer_temperatura_eliminado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            aire.establecer_temperatura(20)

    def test_aire_acondicionado_establecer_temperatura_tipo_invalido(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        with pytest.raises(TypeError, match="debe ser un número entero"):
            aire.establecer_temperatura("20")

    def test_aire_acondicionado_establecer_temperatura_rango_invalido_bajo(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        with pytest.raises(ValueError, match="debe estar entre 16°C y 30°C"):
            aire.establecer_temperatura(15)

    def test_aire_acondicionado_establecer_temperatura_rango_invalido_alto(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        with pytest.raises(ValueError, match="debe estar entre 16°C y 30°C"):
            aire.establecer_temperatura(31)

    def test_aire_acondicionado_establecer_temperatura_valores_limite(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        resultado_min = aire.establecer_temperatura(16)
        assert aire.get_temperatura_objetivo() == 16
        
        resultado_max = aire.establecer_temperatura(30)
        assert aire.get_temperatura_objetivo() == 30

    def test_aire_acondicionado_activar_modo_eco_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, False)
        aire.encender()
        
        resultado = aire.activar_modo_eco()
        
        assert "activado correctamente" in resultado
        assert aire.get_modo_eco() is True

    def test_aire_acondicionado_activar_modo_eco_ya_activado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        with pytest.raises(ValueError, match="ya está activado"):
            aire.activar_modo_eco()

    def test_aire_acondicionado_activar_modo_eco_apagado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, False)
        assert aire.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagado"):
            aire.activar_modo_eco()

    def test_aire_acondicionado_activar_modo_eco_eliminado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, False)
        aire._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            aire.activar_modo_eco()

    def test_aire_acondicionado_desactivar_modo_eco_exitoso(self):
        """Test de desactivación de modo eco exitosa"""
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        resultado = aire.desactivar_modo_eco()
        
        assert "desactivado correctamente" in resultado
        assert aire.get_modo_eco() is False

    def test_aire_acondicionado_desactivar_modo_eco_ya_desactivado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, False)
        aire.encender()
        
        with pytest.raises(ValueError, match="ya está desactivado"):
            aire.desactivar_modo_eco()

    def test_aire_acondicionado_desactivar_modo_eco_apagado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        assert aire.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagado"):
            aire.desactivar_modo_eco()

    def test_aire_acondicionado_desactivar_modo_eco_eliminado(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminado"):
            aire.desactivar_modo_eco()

    def test_aire_acondicionado_crear_dispositivo_temperatura_invalida_baja(self):
        aire = AireAcondicionado()
        
        with pytest.raises(ValueError, match="debe estar entre 16°C y 30°C"):
            aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 15, True)

    def test_aire_acondicionado_crear_dispositivo_temperatura_invalida_alta(self):
        aire = AireAcondicionado()
        
        with pytest.raises(ValueError, match="debe estar entre 16°C y 30°C"):
            aire.crear_dispositivo("Aire Test", "Samsung", "AR12", 2000.0, 1, 31, True)

    def test_aire_acondicionado_buscar_por_nombre_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        
        resultado = aire.buscar_por_nombre("Aire Sala")
        
        assert resultado == "Aire Sala"

    def test_aire_acondicionado_buscar_por_nombre_vacio(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            aire.buscar_por_nombre("")

    def test_aire_acondicionado_eliminar_por_nombre_exitoso(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        
        resultado = aire.eliminar_por_nombre("Aire Sala")
        
        assert "marcado como eliminado" in resultado
        assert aire._eliminado is True

    def test_aire_acondicionado_eliminar_por_nombre_vacio(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            aire.eliminar_por_nombre("")

    def test_aire_acondicionado_str_representacion(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        
        resultado = str(aire)
        
        assert "Aire Sala" in resultado
        assert "Samsung" in resultado
        assert "AR12" in resultado
        assert "Apagado" in resultado
        assert "temperatura=22°C" in resultado
        assert "modo_eco=Activado" in resultado
        assert "2000.0" in resultado
        assert "usuario_id=1" in resultado

    def test_aire_acondicionado_str_representacion_encendido(self):
        aire = AireAcondicionado()
        aire.crear_dispositivo("Aire Sala", "Samsung", "AR12", 2000.0, 1, 22, True)
        aire.encender()
        
        resultado = str(aire)
        
        assert "Encendido" in resultado

    def test_aire_acondicionado_fixture(self, aire_acondicionado_test):
        assert aire_acondicionado_test.get_nombre() == "Aire Sala"
        assert aire_acondicionado_test.get_marca() == "Samsung"
        assert aire_acondicionado_test.get_modelo() == "AR12"
        assert aire_acondicionado_test.get_consumo_energetico() == 2000.0
        assert aire_acondicionado_test.get_id_usuario() == 1
        assert aire_acondicionado_test.get_temperatura_objetivo() == 22
        assert aire_acondicionado_test.get_modo_eco() is True
        assert aire_acondicionado_test.get_id_dispositivo() == 2
