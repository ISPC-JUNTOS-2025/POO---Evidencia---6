import pytest
from datetime import date, datetime
from dominio.usuario import Usuario
from enums.Rol import Rol


class TestUsuario:
    """Tests para la clase Usuario"""

    def test_usuario_creacion_basica(self):
        """Test de creación básica de usuario"""
        usuario = Usuario()
        assert usuario.get_nombre() is None
        assert usuario.get_apellido() is None
        assert usuario.get_email() is None
        assert usuario.get_rol() == Rol.USUARIO
        assert usuario.get_lista_de_domicilios() == []

    def test_usuario_registrar_usuario_exitoso(self):
        """Test de registro exitoso de usuario"""
        usuario = Usuario()
        resultado = usuario.registrar_usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            contraseña="juan123",
            calle="Calle Test",
            numero="123"
        )
        
        assert isinstance(resultado, dict)
        assert resultado['nombre'] == "Juan"
        assert resultado['apellido'] == "Pérez"
        assert resultado['email'] == "juan@test.com"
        assert resultado['rol'] == Rol.USUARIO.value
        assert 'fecha_creacion' in resultado
        assert 'direcciones' in resultado

    def test_usuario_registrar_usuario_nombre_vacio(self):
        """Test de registro con nombre vacío"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            usuario.registrar_usuario("", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")

    def test_usuario_registrar_usuario_apellido_vacio(self):
        """Test de registro con apellido vacío"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="El apellido no puede estar vacío"):
            usuario.registrar_usuario("Juan", "", "juan@test.com", "juan123", "Calle Test", "123")

    def test_usuario_registrar_usuario_email_vacio(self):
        """Test de registro con email vacío"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="El email no puede estar vacío"):
            usuario.registrar_usuario("Juan", "Pérez", "", "juan123", "Calle Test", "123")

    def test_usuario_registrar_usuario_contraseña_vacia(self):
        """Test de registro con contraseña vacía"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="La contraseña no puede estar vacía"):
            usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "", "Calle Test", "123")

    def test_usuario_registrar_usuario_calle_vacia(self):
        """Test de registro con calle vacía"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="La calle no puede estar vacía"):
            usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "", "123")

    def test_usuario_registrar_usuario_numero_vacio(self):
        """Test de registro con número vacío"""
        usuario = Usuario()
        
        with pytest.raises(ValueError, match="El número no puede estar vacío"):
            usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "")

    def test_usuario_iniciar_sesion_exitoso(self):
        """Test de inicio de sesión exitoso"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        resultado = usuario.iniciar_sesion("juan@test.com", "juan123")
        
        assert isinstance(resultado, dict)
        assert resultado['nombre'] == "Juan"
        assert resultado['apellido'] == "Pérez"
        assert resultado['email'] == "juan@test.com"
        assert resultado['rol'] == Rol.USUARIO.value

    def test_usuario_iniciar_sesion_email_incorrecto(self):
        """Test de inicio de sesión con email incorrecto"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="Email o contraseña incorrectos"):
            usuario.iniciar_sesion("otro@test.com", "juan123")

    def test_usuario_iniciar_sesion_contraseña_incorrecta(self):
        """Test de inicio de sesión con contraseña incorrecta"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="Email o contraseña incorrectos"):
            usuario.iniciar_sesion("juan@test.com", "contraseña_incorrecta")

    def test_usuario_iniciar_sesion_email_vacio(self):
        """Test de inicio de sesión con email vacío"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="El email o la contraseña no pueden estar vacíos"):
            usuario.iniciar_sesion("", "juan123")

    def test_usuario_iniciar_sesion_contraseña_vacia(self):
        """Test de inicio de sesión con contraseña vacía"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="El email o la contraseña no pueden estar vacíos"):
            usuario.iniciar_sesion("juan@test.com", "")

    def test_usuario_consultar_datos_personales(self):
        """Test de consulta de datos personales"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        usuario._id_usuario = 1
        
        resultado = usuario.consultar_datos_personales()
        
        assert isinstance(resultado, dict)
        assert resultado['id_usuario'] == 1
        assert resultado['nombre'] == "Juan"
        assert resultado['apellido'] == "Pérez"
        assert resultado['email'] == "juan@test.com"
        assert resultado['rol'] == Rol.USUARIO.value
        assert 'fecha_creacion' in resultado
        assert 'cantidad_domicilios' in resultado

    def test_usuario_setters_y_getters(self):
        """Test de setters y getters"""
        usuario = Usuario()
        
        # Test setters
        usuario.set_nombre("Carlos")
        usuario.set_apellido("García")
        usuario.set_email("carlos@test.com")
        usuario.set_rol(Rol.ADMINISTRADOR)
        
        # Test getters
        assert usuario.get_nombre() == "Carlos"
        assert usuario.get_apellido() == "García"
        assert usuario.get_email() == "carlos@test.com"
        assert usuario.get_rol() == Rol.ADMINISTRADOR

    def test_usuario_set_nombre_trim_espacios(self):
        """Test de trim de espacios en nombre"""
        usuario = Usuario()
        usuario.set_nombre("  Carlos  ")
        assert usuario.get_nombre() == "Carlos"

    def test_usuario_set_apellido_trim_espacios(self):
        """Test de trim de espacios en apellido"""
        usuario = Usuario()
        usuario.set_apellido("  García  ")
        assert usuario.get_apellido() == "García"

    def test_usuario_set_email_trim_espacios(self):
        """Test de trim de espacios en email"""
        usuario = Usuario()
        usuario.set_email("  carlos@test.com  ")
        assert usuario.get_email() == "carlos@test.com"

    def test_usuario_agregar_domicilio(self):
        """Test de agregar domicilio"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        resultado = usuario.agregar_domicilio("Calle Nueva 456")
        
        assert resultado is True
        assert "Calle Nueva 456" in usuario.get_lista_de_domicilios()

    def test_usuario_agregar_domicilio_duplicado(self):
        """Test de agregar domicilio duplicado"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        usuario.agregar_domicilio("Calle Nueva 456")
        
        resultado = usuario.agregar_domicilio("Calle Nueva 456")
        
        assert resultado is True  # Retorna True pero no agrega duplicado
        assert usuario.get_lista_de_domicilios().count("Calle Nueva 456") == 1

    def test_usuario_agregar_domicilio_nulo(self):
        """Test de agregar domicilio nulo"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="El domicilio no puede ser nulo"):
            usuario.agregar_domicilio(None)

    def test_usuario_remover_domicilio(self):
        """Test de remover domicilio"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        usuario.agregar_domicilio("Calle Nueva 456")
        
        resultado = usuario.remover_domicilio("Calle Nueva 456")
        
        assert resultado is True
        assert "Calle Nueva 456" not in usuario.get_lista_de_domicilios()

    def test_usuario_remover_domicilio_inexistente(self):
        """Test de remover domicilio inexistente"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        resultado = usuario.remover_domicilio("Calle Inexistente 999")
        
        assert resultado is True  # Retorna True pero no remueve nada

    def test_usuario_remover_domicilio_nulo(self):
        """Test de remover domicilio nulo"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="El domicilio no puede ser nulo"):
            usuario.remover_domicilio(None)

    def test_usuario_cambiar_rol_exitoso(self):
        """Test de cambio de rol exitoso"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        resultado = usuario.cambiar_rol_de_usuario(Rol.ADMINISTRADOR)
        
        assert resultado is True
        assert usuario.get_rol() == Rol.ADMINISTRADOR

    def test_usuario_cambiar_rol_nulo(self):
        """Test de cambio de rol nulo"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        with pytest.raises(ValueError, match="El nuevo rol no puede ser nulo"):
            usuario.cambiar_rol_de_usuario(None)

    def test_usuario_str_representacion(self):
        """Test de representación string"""
        usuario = Usuario()
        usuario.registrar_usuario("Juan", "Pérez", "juan@test.com", "juan123", "Calle Test", "123")
        
        resultado = str(usuario)
        
        assert "Juan" in resultado
        assert "Pérez" in resultado
        assert Rol.USUARIO.value in resultado

    def test_usuario_fixture_admin(self, usuario_admin):
        """Test usando fixture de usuario admin"""
        assert usuario_admin.get_nombre() == "Admin"
        assert usuario_admin.get_apellido() == "Sistema"
        assert usuario_admin.get_email() == "admin@test.com"
        assert usuario_admin.get_rol() == Rol.ADMINISTRADOR
        assert usuario_admin.get_id_usuario() == 1

    def test_usuario_fixture_normal(self, usuario_normal):
        """Test usando fixture de usuario normal"""
        assert usuario_normal.get_nombre() == "Juan"
        assert usuario_normal.get_apellido() == "Pérez"
        assert usuario_normal.get_email() == "juan@test.com"
        assert usuario_normal.get_rol() == Rol.USUARIO
        assert usuario_normal.get_id_usuario() == 2
