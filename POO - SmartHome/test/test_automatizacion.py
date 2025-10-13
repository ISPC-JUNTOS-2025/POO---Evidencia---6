import pytest
from datetime import datetime
from dominio.Automatizacion import Automatizacion
from dominio.luz import Luz


class TestAutomatizacion:
    

    def test_automatizacion_creacion_basica(self):
        
        automatizacion = Automatizacion()
        assert automatizacion.get_id_automatizacion() is None
        assert automatizacion.get_nombre() is None
        assert automatizacion.get_descripcion() is None
        assert automatizacion.get_estado() is False
        assert automatizacion.get_regla() is None
        assert automatizacion.get_condicion() is None
        assert automatizacion.get_accion() is None
        assert automatizacion.get_id_usuario() is None
        assert automatizacion.get_dispositivos_controlados() == []
        assert isinstance(automatizacion.get_fecha_creacion(), datetime)

    def test_automatizacion_crear_automatizacion_exitoso(self):
        
        automatizacion = Automatizacion()
        resultado = automatizacion.crear_automatizacion(
            nombre="Encender Luces",
            descripcion="Encender luces al detectar movimiento",
            regla="Si hay movimiento entonces encender luces",
            condicion="movimiento detectado",
            accion="encender luces",
            id_usuario=1
        )
        
        assert resultado == automatizacion
        assert automatizacion.get_nombre() == "Encender Luces"
        assert automatizacion.get_descripcion() == "Encender luces al detectar movimiento"
        assert automatizacion.get_regla() == "Si hay movimiento entonces encender luces"
        assert automatizacion.get_condicion() == "movimiento detectado"
        assert automatizacion.get_accion() == "encender luces"
        assert automatizacion.get_id_usuario() == 1

    def test_automatizacion_crear_automatizacion_nombre_vacio(self):
        
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            automatizacion.crear_automatizacion("", "Descripción", "Regla", "Condición", "Acción", 1)

    def test_automatizacion_crear_automatizacion_descripcion_vacia(self):
        
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="La descripción no puede estar vacía"):
            automatizacion.crear_automatizacion("Nombre", "", "Regla", "Condición", "Acción", 1)

    def test_automatizacion_crear_automatizacion_regla_vacia(self):
        
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="La regla no puede estar vacía"):
            automatizacion.crear_automatizacion("Nombre", "Descripción", "", "Condición", "Acción", 1)

    def test_automatizacion_crear_automatizacion_condicion_vacia(self):
        
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="La condición no puede estar vacía"):
            automatizacion.crear_automatizacion("Nombre", "Descripción", "Regla", "", "Acción", 1)

    def test_automatizacion_crear_automatizacion_accion_vacia(self):
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="La acción no puede estar vacía"):
            automatizacion.crear_automatizacion("Nombre", "Descripción", "Regla", "Condición", "", 1)

    def test_automatizacion_crear_automatizacion_id_usuario_invalido(self):
        automatizacion = Automatizacion()
        
        with pytest.raises(ValueError, match="El ID de usuario debe ser válido"):
            automatizacion.crear_automatizacion("Nombre", "Descripción", "Regla", "Condición", "Acción", 0)

    def test_automatizacion_setters_y_getters(self):
        automatizacion = Automatizacion()
        
        # Test setters
        automatizacion.set_id_automatizacion(1)
        automatizacion.set_nombre("Test Automatización")
        automatizacion.set_descripcion("Descripción de prueba")
        automatizacion.set_estado(True)
        automatizacion.set_regla("Regla de prueba")
        automatizacion.set_condicion("Condición de prueba")
        automatizacion.set_accion("Acción de prueba")
        automatizacion.set_id_usuario(1)
        
        # Test getters
        assert automatizacion.get_id_automatizacion() == 1
        assert automatizacion.get_nombre() == "Test Automatización"
        assert automatizacion.get_descripcion() == "Descripción de prueba"
        assert automatizacion.get_estado() is True
        assert automatizacion.get_regla() == "Regla de prueba"
        assert automatizacion.get_condicion() == "Condición de prueba"
        assert automatizacion.get_accion() == "Acción de prueba"
        assert automatizacion.get_id_usuario() == 1

    def test_automatizacion_agregar_dispositivo_exitoso(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        
        resultado = automatizacion.agregar_dispositivo(luz)
        
        assert resultado is True
        assert luz in automatizacion.get_dispositivos_controlados()
        assert len(automatizacion.get_dispositivos_controlados()) == 1

    def test_automatizacion_agregar_dispositivo_duplicado(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        with pytest.raises(ValueError, match="ya está en esta automatización"):
            automatizacion.agregar_dispositivo(luz)

    def test_automatizacion_agregar_dispositivo_nulo(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        with pytest.raises(ValueError, match="El dispositivo no puede ser nulo"):
            automatizacion.agregar_dispositivo(None)

    def test_automatizacion_remover_dispositivo_exitoso(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.remover_dispositivo(luz)
        
        assert resultado is True
        assert luz not in automatizacion.get_dispositivos_controlados()
        assert len(automatizacion.get_dispositivos_controlados()) == 0

    def test_automatizacion_remover_dispositivo_inexistente(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        
        with pytest.raises(ValueError, match="no está en esta automatización"):
            automatizacion.remover_dispositivo(luz)

    def test_automatizacion_remover_dispositivo_nulo(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        with pytest.raises(ValueError, match="El dispositivo no puede ser nulo"):
            automatizacion.remover_dispositivo(None)

    def test_automatizacion_activar_encender_luces_exitoso(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.activar_automatizacion_encender_luces()
        
        assert resultado is True
        assert automatizacion.get_estado() is True
        assert luz.get_activado() is True
        assert luz.get_intensidad() == 80

    def test_automatizacion_activar_encender_luces_ya_activa(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        with pytest.raises(ValueError, match="ya está activa"):
            automatizacion.activar_automatizacion_encender_luces()

    def test_automatizacion_activar_encender_luces_sin_luces(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        
        with pytest.raises(ValueError, match="No hay luces configuradas"):
            automatizacion.activar_automatizacion_encender_luces()

    def test_automatizacion_desactivar_encender_luces_exitoso(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.desactivar_automatizacion_encender_luces()
        
        assert resultado is True
        assert automatizacion.get_estado() is False
        assert luz.get_activado() is False

    def test_automatizacion_desactivar_encender_luces_ya_desactivada(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(False)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        with pytest.raises(ValueError, match="ya está desactivada"):
            automatizacion.desactivar_automatizacion_encender_luces()

    def test_automatizacion_desactivar_encender_luces_sin_luces(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(True)
        
        with pytest.raises(ValueError, match="No hay luces configuradas"):
            automatizacion.desactivar_automatizacion_encender_luces()

    def test_automatizacion_consultar_automatizaciones_activas(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        automatizacion.set_id_automatizacion(1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.consultar_automatizaciones_activas()
        
        assert isinstance(resultado, dict)
        assert resultado['id_automatizacion'] == 1
        assert resultado['nombre'] == "Test"
        assert resultado['descripcion'] == "Desc"
        assert resultado['estado'] == "Activa"
        assert resultado['regla'] == "Regla"
        assert resultado['condicion'] == "Cond"
        assert resultado['accion'] == "Acc"
        assert resultado['dispositivos_controlados'] == 1

    def test_automatizacion_mostrar_informacion_automatizacion(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.mostrar_informacion_automatizacion()
        
        assert isinstance(resultado, str)
        assert "Test" in resultado
        assert "Activa" in resultado
        assert "Desc" in resultado
        assert "Regla" in resultado
        assert "Cond" in resultado
        assert "Acc" in resultado
        assert "Luz Test" in resultado

    def test_automatizacion_ejecutar_automatizacion_encender_luces(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.ejecutar_automatizacion()
        
        assert resultado is True
        assert luz.get_activado() is True

    def test_automatizacion_ejecutar_automatizacion_apagar_luces(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "apagar luces", 1)
        automatizacion.set_estado(True)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        luz.encender()
        automatizacion.agregar_dispositivo(luz)
        
        resultado = automatizacion.ejecutar_automatizacion()
        
        assert resultado is True
        assert luz.get_activado() is False

    def test_automatizacion_ejecutar_automatizacion_desactivada(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "encender luces", 1)
        automatizacion.set_estado(False)
        
        with pytest.raises(ValueError, match="está desactivada"):
            automatizacion.ejecutar_automatizacion()

    def test_automatizacion_ejecutar_automatizacion_tipo_no_reconocido(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "acción desconocida", 1)
        automatizacion.set_estado(True)
        
        with pytest.raises(ValueError, match="Tipo de automatización no reconocido"):
            automatizacion.ejecutar_automatizacion()

    def test_automatizacion_validar_condicion_movimiento(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "movimiento detectado", "Acc", 1)
        
        # Test con movimiento detectado
        resultado_true = automatizacion.validar_condicion(True)
        assert resultado_true is True
        
        # Test sin movimiento
        resultado_false = automatizacion.validar_condicion(False)
        assert resultado_false is False
        
        # Test con valor nulo
        resultado_none = automatizacion.validar_condicion(None)
        assert resultado_none is False

    def test_automatizacion_validar_condicion_hora(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "hora específica", "Acc", 1)
        
        resultado = automatizacion.validar_condicion()
        
        assert resultado is True

    def test_automatizacion_validar_condicion_temperatura(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "temperatura alta", "Acc", 1)
        
        resultado = automatizacion.validar_condicion()
        
        assert resultado is True

    def test_automatizacion_validar_condicion_default(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "condición desconocida", "Acc", 1)
        
        resultado = automatizacion.validar_condicion()
        
        assert resultado is True

    def test_automatizacion_str_representacion(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test Automatización", "Descripción de prueba", "Regla", "Cond", "Acc", 1)
        automatizacion.set_estado(True)
        
        resultado = str(automatizacion)
        
        assert "Test Automatización" in resultado
        assert "Activa" in resultado
        assert "Descripción de prueba" in resultado

    def test_automatizacion_str_representacion_inactiva(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test Automatización", "Descripción de prueba", "Regla", "Cond", "Acc", 1)
        automatizacion.set_estado(False)
        
        resultado = str(automatizacion)
        
        assert "Test Automatización" in resultado
        assert "Inactiva" in resultado
        assert "Descripción de prueba" in resultado

    def test_automatizacion_dispositivos_controlados_copia_segura(self):
        automatizacion = Automatizacion()
        automatizacion.crear_automatizacion("Test", "Desc", "Regla", "Cond", "Acc", 1)
        
        luz = Luz()
        luz.crear_dispositivo("Luz Test", "Philips", "Hue", 15.5, 1, 80, True)
        automatizacion.agregar_dispositivo(luz)
        
        dispositivos1 = automatizacion.get_dispositivos_controlados()
        dispositivos2 = automatizacion.get_dispositivos_controlados()
        
        assert dispositivos1 is not dispositivos2  # Diferentes objetos
        assert dispositivos1 == dispositivos2  # Mismo contenido
