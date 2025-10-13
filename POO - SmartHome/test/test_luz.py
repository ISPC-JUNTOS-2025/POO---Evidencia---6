import pytest
from datetime import datetime
from dominio.luz import Luz
from enums.tipodispositivo import TipoDispositivo


class TestLuz:

    def test_luz_creacion_basica(self):
        luz = Luz()
        assert luz.get_nombre() is None
        assert luz.get_marca() is None
        assert luz.get_modelo() is None
        assert luz.get_consumo_energetico() is None
        assert luz.get_id_usuario() is None
        assert luz.get_intensidad() == 100
        assert luz.get_regulable() is False
        assert luz.get_tipo_dispositivo() == TipoDispositivo.LUZ
        assert isinstance(luz.get_fecha_creacion(), datetime)

    def test_luz_crear_dispositivo_exitoso(self):
        luz = Luz()
        resultado = luz.crear_dispositivo(
            nombre="Luz Sala",
            marca="Philips",
            modelo="Hue",
            consumo_energetico=15.5,
            id_usuario=1,
            intensidad=80,
            regulable=True
        )
        
        assert resultado == luz
        assert luz.get_nombre() == "Luz Sala"
        assert luz.get_marca() == "Philips"
        assert luz.get_modelo() == "Hue"
        assert luz.get_consumo_energetico() == 15.5
        assert luz.get_id_usuario() == 1
        assert luz.get_intensidad() == 80
        assert luz.get_regulable() is True

    def test_luz_setters_y_getters(self):
        """Test de setters y getters específicos de luz"""
        luz = Luz()
        
        # Test setters
        luz.set_intensidad(75)
        luz.set_regulable(True)
        
        # Test getters
        assert luz.get_intensidad() == 75
        assert luz.get_regulable() is True

    def test_luz_encender_exitoso(self):
        """Test de encendido exitoso"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        assert luz.get_activado() is False
        
        resultado = luz.encender()
        
        assert "encendida correctamente" in resultado
        assert luz.get_activado() is True

    def test_luz_encender_ya_encendida(self):
        """Test de encendido cuando ya está encendida"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        assert luz.get_activado() is True
        
        with pytest.raises(ValueError, match="ya está encendida"):
            luz.encender()

    def test_luz_apagar_exitoso(self):
        """Test de apagado exitoso"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        assert luz.get_activado() is True
        
        resultado = luz.apagar()
        
        assert "apagada correctamente" in resultado
        assert luz.get_activado() is False

    def test_luz_apagar_ya_apagada(self):
        """Test de apagado cuando ya está apagada"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        assert luz.get_activado() is False
        
        with pytest.raises(ValueError, match="ya está apagada"):
            luz.apagar()

    def test_luz_encender_eliminada(self):
        """Test de encendido cuando está eliminada"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            luz.encender()

    def test_luz_apagar_eliminada(self):
        """Test de apagado cuando está eliminada"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            luz.apagar()

    def test_luz_regular_intensidad_exitoso(self):
        """Test de regulación de intensidad exitosa"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        resultado = luz.regular_intensidad(60)
        
        assert "ajustada a 60%" in resultado
        assert luz.get_intensidad() == 60

    def test_luz_regular_intensidad_apagada(self):
        """Test de regulación de intensidad cuando está apagada"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        assert luz.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagada"):
            luz.regular_intensidad(60)

    def test_luz_regular_intensidad_no_regulable(self):
        """Test de regulación de intensidad cuando no es regulable"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, False)
        luz.encender()
        
        with pytest.raises(ValueError, match="no es regulable"):
            luz.regular_intensidad(60)

    def test_luz_regular_intensidad_eliminada(self):
        """Test de regulación de intensidad cuando está eliminada"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            luz.regular_intensidad(60)

    def test_luz_regular_intensidad_valor_invalido_tipo(self):
        """Test de regulación con valor inválido de tipo"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        with pytest.raises(TypeError, match="debe ser un número entero"):
            luz.regular_intensidad("60")

    def test_luz_regular_intensidad_valor_invalido_rango_negativo(self):
        """Test de regulación con valor fuera de rango (negativo)"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            luz.regular_intensidad(-10)

    def test_luz_regular_intensidad_valor_invalido_rango_alto(self):
        """Test de regulación con valor fuera de rango (alto)"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            luz.regular_intensidad(150)

    def test_luz_regular_intensidad_valores_limite(self):
        """Test de regulación con valores límite"""
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        # Test valor mínimo
        resultado_min = luz.regular_intensidad(0)
        assert luz.get_intensidad() == 0
        
        # Test valor máximo
        resultado_max = luz.regular_intensidad(100)
        assert luz.get_intensidad() == 100

    def test_luz_buscar_por_nombre_exitoso(self):
        """Test de búsqueda por nombre exitosa"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        
        resultado = luz.buscar_por_nombre("Luz Sala")
        
        assert resultado == "Luz Sala"

    def test_luz_buscar_por_nombre_vacio(self):
        """Test de búsqueda con nombre vacío"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            luz.buscar_por_nombre("")

    def test_luz_eliminar_por_nombre_exitoso(self):
        """Test de eliminación por nombre exitosa"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        
        resultado = luz.eliminar_por_nombre("Luz Sala")
        
        assert "marcada como eliminada" in resultado
        assert luz._eliminado is True

    def test_luz_eliminar_por_nombre_vacio(self):
        """Test de eliminación con nombre vacío"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            luz.eliminar_por_nombre("")

    def test_luz_str_representacion(self):
        """Test de representación string"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        
        resultado = str(luz)
        
        assert "Luz Sala" in resultado
        assert "Philips" in resultado
        assert "Hue" in resultado
        assert "Apagada" in resultado
        assert "intensidad=80" in resultado
        assert "regulable=True" in resultado
        assert "15.5" in resultado
        assert "usuario_id=1" in resultado

    def test_luz_str_representacion_encendida(self):
        """Test de representación string cuando está encendida"""
        luz = Luz()
        luz.crear_dispositivo("Luz Sala", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        
        resultado = str(luz)
        
        assert "Encendida" in resultado

    def test_luz_fixture(self, luz_test):
        """Test usando fixture de luz"""
        assert luz_test.get_nombre() == "Luz Sala"
        assert luz_test.get_marca() == "Philips"
        assert luz_test.get_modelo() == "Hue"
        assert luz_test.get_consumo_energetico() == 15.5
        assert luz_test.get_id_usuario() == 1
        assert luz_test.get_intensidad() == 80
        assert luz_test.get_regulable() is True
        assert luz_test.get_id_dispositivo() == 1
