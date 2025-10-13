import pytest
from datetime import datetime
from dominio.camara import Camara
from enums.tipodispositivo import TipoDispositivo


class TestCamara:

    def test_camara_creacion_basica(self):
        camara = Camara()
        assert camara.get_nombre() is None
        assert camara.get_marca() is None
        assert camara.get_modelo() is None
        assert camara.get_consumo_energetico() is None
        assert camara.get_id_usuario() is None
        assert camara.get_resolucion() == "1080p"
        assert camara.get_vision_nocturna() is True
        assert camara.get_grabacion() is False
        assert camara.get_almacenamiento_local() is True
        assert camara.get_tipo_dispositivo() == TipoDispositivo.DISPOSITIVO_DE_GRABACION
        assert isinstance(camara.get_fecha_creacion(), datetime)

    def test_camara_crear_dispositivo_exitoso(self):
        camara = Camara()
        resultado = camara.crear_dispositivo(
            nombre="Cámara Entrada",
            marca="Ring",
            modelo="Video Doorbell",
            consumo_energetico=5.0,
            id_usuario=1,
            resolucion="1080p",
            vision_nocturna=True,
            almacenamiento_local=True
        )
        
        assert resultado == camara
        assert camara.get_nombre() == "Cámara Entrada"
        assert camara.get_marca() == "Ring"
        assert camara.get_modelo() == "Video Doorbell"
        assert camara.get_consumo_energetico() == 5.0
        assert camara.get_id_usuario() == 1
        assert camara.get_resolucion() == "1080p"
        assert camara.get_vision_nocturna() is True
        assert camara.get_almacenamiento_local() is True

    def test_camara_setters_y_getters(self):
        camara = Camara()
        
        # Test setters
        camara.set_resolucion("4K")
        camara.set_vision_nocturna(False)
        camara.set_grabacion(True)
        camara.set_almacenamiento_local(False)
        
        # Test getters
        assert camara.get_resolucion() == "4K"
        assert camara.get_vision_nocturna() is False
        assert camara.get_grabacion() is True
        assert camara.get_almacenamiento_local() is False

    def test_camara_encender_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        assert camara.get_activado() is False
        
        resultado = camara.encender()
        
        assert "encendida correctamente" in resultado
        assert "Resolución: 1080p" in resultado
        assert camara.get_activado() is True

    def test_camara_encender_ya_encendida(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        assert camara.get_activado() is True
        
        with pytest.raises(ValueError, match="ya está encendida"):
            camara.encender()

    def test_camara_apagar_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        assert camara.get_activado() is True
        
        resultado = camara.apagar()
        
        assert "apagada correctamente" in resultado
        assert camara.get_activado() is False

    def test_camara_apagar_ya_apagada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        assert camara.get_activado() is False
        
        with pytest.raises(ValueError, match="ya está apagada"):
            camara.apagar()

    def test_camara_apagar_detiene_grabacion(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        assert camara.get_grabacion() is True
        
        camara.apagar()
        
        assert camara.get_grabacion() is False

    def test_camara_encender_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.encender()

    def test_camara_apagar_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.apagar()

    def test_camara_iniciar_grabacion_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        
        resultado = camara.iniciar_grabacion()
        
        assert "iniciando grabación en 1080p" in resultado
        assert camara.get_grabacion() is True

    def test_camara_iniciar_grabacion_ya_grabando(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        
        with pytest.raises(ValueError, match="ya está grabando"):
            camara.iniciar_grabacion()

    def test_camara_iniciar_grabacion_apagada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        assert camara.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagada"):
            camara.iniciar_grabacion()

    def test_camara_iniciar_grabacion_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.iniciar_grabacion()

    def test_camara_detener_grabacion_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        
        resultado = camara.detener_grabacion()
        
        assert "deteniendo grabación" in resultado
        assert "almacenamiento local" in resultado
        assert camara.get_grabacion() is False

    def test_camara_detener_grabacion_almacenamiento_nube(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, False)
        camara.encender()
        camara.iniciar_grabacion()
        
        resultado = camara.detener_grabacion()
        
        assert "nube" in resultado

    def test_camara_detener_grabacion_no_grabando(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        
        with pytest.raises(ValueError, match="no está grabando"):
            camara.detener_grabacion()

    def test_camara_detener_grabacion_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.detener_grabacion()

    def test_camara_cambiar_resolucion_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        resultado = camara.cambiar_resolucion("4K")
        
        assert "cambiada a 4K" in resultado
        assert camara.get_resolucion() == "4K"

    def test_camara_cambiar_resolucion_grabando(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        
        with pytest.raises(RuntimeError, match="está grabando"):
            camara.cambiar_resolucion("4K")

    def test_camara_cambiar_resolucion_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.cambiar_resolucion("4K")

    def test_camara_cambiar_resolucion_invalida(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        with pytest.raises(ValueError, match="debe ser una de"):
            camara.cambiar_resolucion("720i")

    def test_camara_cambiar_resolucion_valores_validos(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        resoluciones_validas = ["720p", "1080p", "2K", "4K"]
        for resolucion in resoluciones_validas:
            resultado = camara.cambiar_resolucion(resolucion)
            assert f"cambiada a {resolucion}" in resultado
            assert camara.get_resolucion() == resolucion

    def test_camara_activar_vision_nocturna_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", False, True)
        camara.encender()
        
        resultado = camara.activar_vision_nocturna()
        
        assert "activada correctamente" in resultado
        assert camara.get_vision_nocturna() is True

    def test_camara_activar_vision_nocturna_ya_activada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        
        with pytest.raises(ValueError, match="ya está activada"):
            camara.activar_vision_nocturna()

    def test_camara_activar_vision_nocturna_apagada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", False, True)
        assert camara.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagada"):
            camara.activar_vision_nocturna()

    def test_camara_activar_vision_nocturna_eliminada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", False, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.activar_vision_nocturna()

    def test_camara_desactivar_vision_nocturna_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        
        resultado = camara.desactivar_vision_nocturna()
        
        assert "desactivada correctamente" in resultado
        assert camara.get_vision_nocturna() is False

    def test_camara_desactivar_vision_nocturna_ya_desactivada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", False, True)
        camara.encender()
        
        with pytest.raises(ValueError, match="ya está desactivada"):
            camara.desactivar_vision_nocturna()

    def test_camara_desactivar_vision_nocturna_apagada(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        assert camara.get_activado() is False
        
        with pytest.raises(RuntimeError, match="está apagada"):
            camara.desactivar_vision_nocturna()

    def test_camara_desactivar_vision_nocturna_eliminada(self):

        camara = Camara()
        camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara._eliminado = True
        
        with pytest.raises(RuntimeError, match="porque está eliminada"):
            camara.desactivar_vision_nocturna()

    def test_camara_crear_dispositivo_resolucion_invalida(self):
        camara = Camara()
        
        with pytest.raises(ValueError, match="debe ser una de"):
            camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "720i", True, True)

    def test_camara_crear_dispositivo_resolucion_vacia(self):
        camara = Camara()
        
        with pytest.raises(ValueError, match="no puede estar vacía"):
            camara.crear_dispositivo("Cámara Test", "Ring", "Video Doorbell", 5.0, 1, "", True, True)

    def test_camara_buscar_por_nombre_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        resultado = camara.buscar_por_nombre("Cámara Entrada")
        
        assert resultado == "Cámara Entrada"

    def test_camara_buscar_por_nombre_vacio(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            camara.buscar_por_nombre("")

    def test_camara_eliminar_por_nombre_exitoso(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        
        resultado = camara.eliminar_por_nombre("Cámara Entrada")
        
        assert "marcada como eliminada" in resultado
        assert camara._eliminado is True
        assert camara.get_grabacion() is False  # Debe detener grabación

    def test_camara_eliminar_por_nombre_vacio(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            camara.eliminar_por_nombre("")

    def test_camara_str_representacion(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        
        resultado = str(camara)
        
        assert "Cámara Entrada" in resultado
        assert "Ring" in resultado
        assert "Video Doorbell" in resultado
        assert "Apagada" in resultado
        assert "En espera" in resultado
        assert "resolucion=1080p" in resultado
        assert "vision_nocturna=Activada" in resultado
        assert "almacenamiento=Local" in resultado
        assert "5.0" in resultado
        assert "usuario_id=1" in resultado

    def test_camara_str_representacion_encendida_grabando(self):
        camara = Camara()
        camara.crear_dispositivo("Cámara Entrada", "Ring", "Video Doorbell", 5.0, 1, "1080p", True, True)
        camara.encender()
        camara.iniciar_grabacion()
        
        resultado = str(camara)
        
        assert "Encendida" in resultado
        assert "Grabando" in resultado

    def test_camara_fixture(self, camara_test):
        assert camara_test.get_nombre() == "Cámara Entrada"
        assert camara_test.get_marca() == "Ring"
        assert camara_test.get_modelo() == "Video Doorbell"
        assert camara_test.get_consumo_energetico() == 5.0
        assert camara_test.get_id_usuario() == 1
        assert camara_test.get_resolucion() == "1080p"
        assert camara_test.get_vision_nocturna() is True
        assert camara_test.get_almacenamiento_local() is True
        assert camara_test.get_id_dispositivo() == 3
