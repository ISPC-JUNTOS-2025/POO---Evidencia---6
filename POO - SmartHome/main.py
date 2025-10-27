from dominio.usuario import Usuario
from enums.Rol import Rol
from dao.usuario_dao import UsuarioDao
from dao.dispositivo_dao import DispositivoDAO
from dominio.luz import Luz 
from dominio.aire_acondicionado import AireAcondicionado
from dominio.camara import Camara
from dominio.sensor_movimiento import SensorMovimiento
from enums.tipodispositivo import TipoDispositivo
import sys

usuario_dao = UsuarioDao()
dispositivo_dao = DispositivoDAO()


def registrar_usuario():
    print("\n=== Registro de nuevo usuario ===")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email: ").strip()
    contraseña = input("Contraseña: ").strip()
    calle = input("Calle: ").strip()
    numero = input("Número: ").strip()

    nuevo_usuario = Usuario()
    try:
        nuevo_usuario.registrar_usuario(nombre, apellido, email, contraseña, calle, numero)
        usuario_dao.crear(nuevo_usuario)
        print("\n Usuario registrado correctamente.")
    except Exception as e:
        print(f"\n Error: {e}")


def iniciar_sesion():
    print("\n=== Inicio de sesión ===")
    email = input("Email: ").strip()
    contraseña = input("Contraseña: ").strip()
    
    usuarios = usuario_dao.buscar_usuarios()
    for u in usuarios:
        if u.get_email() == email.lower():
            try:
                sesion = u.iniciar_sesion(email, contraseña)
                print(f"\n Bienvenido {sesion['nombre']} {sesion['apellido']} ({u.get_rol().value})")
                return u
            except ValueError as e:
                print(f" Error: {e}")
                return None
            except Exception as e:
                print(f" Error al iniciar sesión: {e}")
                return None
    
    print(" Usuario no encontrado.")
    return None


def menu_usuario(usuario: Usuario):
    while True:
        print(f"\n=== Menú Usuario ({usuario.get_nombre()}) ===")
        print("1. Consultar datos personales")
        print("2. Consultar dispositivos")
        print("3. Cerrar sesión")

        opcion = input("\nElija una opción: ").strip()
        
        match opcion:
            case "1":
                try:
                    datos = usuario.consultar_datos_personales()
                    print("\n--- Datos Personales ---")
                    for k, v in datos.items():
                        print(f"{k.capitalize()}: {v}")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "2":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    
                    if dispositivos:
                        print("\n--- Todos los dispositivos ---")
                        for d in dispositivos:
                            estado = "Encendido" if d.get("activado") else "Apagado"
                            print(f"• {d['nombre']} ({d['tipo_dispositivo']}) - {estado}")
                            print(f"  Marca: {d['marca']} | Modelo: {d['modelo']}")
                            print(f"  Consumo: {d['consumo_energetico']} W")
                            print(f"  Propietario: {d.get('nombre_usuario', 'N/A')}\n")
                    else:
                        print("\n✗ No hay dispositivos registrados en el sistema.")
                except Exception as e:
                    print(f"✗ Error al consultar dispositivos: {e}")

            case "3":
                print("✓ Cerrando sesión...")
                break
                
            case _:
                print("✗ Opción inválida.")


def menu_admin(usuario: Usuario):
    while True:
        print(f"\n=== Menú Administrador ({usuario.get_nombre()}) ===")
        print("1. Listar todos los dispositivos")
        print("2. Crear nuevo dispositivo")
        print("3. Actualizar dispositivo")
        print("4. Eliminar dispositivo")
        print("5. Cambiar rol de usuario")
        print("6. Cerrar sesión")

        opcion = input("\nElija una opción: ").strip()

        match opcion:
            case "1":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    if dispositivos:
                        print("\n--- Lista de dispositivos ---")
                        for d in dispositivos:
                            estado = "Encendido" if d.get("activado") else "Apagado"
                            print(f"• {d['nombre']} ({d['tipo_dispositivo']}) - {estado}")
                            print(f"  Propietario: {d.get('nombre_usuario', 'N/A')} | Marca: {d['marca']} | Modelo: {d['modelo']}")
                            print(f"  Consumo: {d['consumo_energetico']} W\n")
                    else:
                        print("\nNo hay dispositivos registrados.")
                except Exception as e:
                    print(f"Error: {e}")

            case "2":
                try:
                    print("\n--- Crear dispositivo ---")
                    nombre = input("Nombre: ").strip()
                    marca = input("Marca: ").strip()
                    modelo = input("Modelo: ").strip()
                    consumo = float(input("Consumo energético (W): "))
                    id_usuario = usuario.get_id_usuario()

                    print("\nTipos de dispositivo:")
                    tipos = list(TipoDispositivo)
                    for i, tipo in enumerate(tipos, 1):
                        print(f"{i}. {tipo.value}")
                    
                    opcion_tipo = input("Seleccione tipo: ").strip()

                    match opcion_tipo:
                        case "1":
                            intensidad = int(input("Intensidad (0-100): "))
                            regulable = input("¿Es regulable? (s/n): ").lower() == "s"
                            
                            nuevo = Luz()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, intensidad, regulable)

                        case "2":
                            modo_eco = input("¿Modo eco? (s/n): ").lower() == "s"
                            
                            nuevo = AireAcondicionado()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, 0, modo_eco)

                        case "3":
                            sensibilidad = int(input("Sensibilidad (0-100): "))
                            rango = float(input("Rango de detección (metros): "))
                            
                            nuevo = SensorMovimiento()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, sensibilidad, rango)

                        case "4":
                            print("Resoluciones: 720p, 1080p, 2K, 4K")
                            resolucion = input("Resolución: ").strip()
                            vision_nocturna = input("¿Visión nocturna? (s/n): ").lower() == "s"
                            
                            nuevo = Camara()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, resolucion, vision_nocturna, True)
                            
                        case _:
                            print("✗ Tipo de dispositivo inválido.")
                            continue

                    dispositivo_dao.crear(nuevo)
                    print("Dispositivo creado con éxito.")
                    
                except ValueError as e:
                    print(f"Error en los datos ingresados: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            case "3":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    if dispositivos:
                        print("\n--- Dispositivos disponibles ---")
                        for d in dispositivos:
                            print(f"• {d['nombre']} ({d['tipo_dispositivo']}) - Propietario: {d.get('nombre_usuario', 'N/A')}")
                    
                    nombre_dispositivo = input("\nNombre del dispositivo a actualizar: ").strip()
                    dispositivo_actual = next((d for d in dispositivos if d['nombre'] == nombre_dispositivo), None)
                    
                    if not dispositivo_actual:
                        print("Dispositivo no encontrado.")
                        continue
                    
                    nombre = input("Nuevo nombre: ").strip()
                    marca = input("Nueva marca: ").strip()
                    modelo = input("Nuevo modelo: ").strip()
                    consumo = float(input("Nuevo consumo energético (W): "))
                    
                    tipo = dispositivo_actual['tipo_dispositivo']
                    
                    match tipo:
                        case "Luz":
                            d = Luz()
                            d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], 100, False)
                        case "Electrodomestico":
                            d = AireAcondicionado()
                            d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], 0, False)
                        case "Dispositivo De Grabacion":
                            d = Camara()
                            d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], "1080p", True, True)
                        case "Sensor":
                            d = SensorMovimiento()
                            d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], 50, 5.0)
                        case _:
                            print("Tipo de dispositivo no reconocido.")
                            continue
                    
                    d._id_dispositivo = dispositivo_actual['id_dispositivo']
                    
                    dispositivo_dao.actualizar(d)
                    print("Dispositivo actualizado.")
                        
                except ValueError as e:
                    print(f"Error en los datos: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            case "4":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    if dispositivos:
                        print("\n--- Dispositivos disponibles ---")
                        for d in dispositivos:
                            print(f"• {d['nombre']} ({d['tipo_dispositivo']}) - Propietario: {d.get('nombre_usuario', 'N/A')}")
                    
                    nombre_dispositivo = input("\nNombre del dispositivo a eliminar: ").strip()
                    dispositivo_actual = next((d for d in dispositivos if d['nombre'] == nombre_dispositivo), None)
                    
                    if not dispositivo_actual:
                        print("Dispositivo no encontrado.")
                        continue
                    
                    confirmacion = input(f"¿Está seguro de eliminar el dispositivo '{nombre_dispositivo}'? (s/n): ").lower()
                    
                    if confirmacion == 's':
                        if dispositivo_dao.eliminar(dispositivo_actual['id_dispositivo']):
                            print("Dispositivo eliminado.")
                        else:
                            print("No se encontró el dispositivo.")
                    else:
                        print("Operación cancelada.")
                        
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            case "5":
                try:
                    usuarios = usuario_dao.buscar_usuarios()
                    print("\n--- Usuarios ---")
                    for u in usuarios:
                        print(f"• {u.get_nombre()} {u.get_apellido()} ({u.get_rol().value}) - {u.get_email()}")

                    nombre_u = input("\nNombre del usuario a cambiar rol: ").strip()
                    apellido_u = input("Apellido del usuario: ").strip()
                    
                    usuario_obj = usuario_dao.buscar_usuario_por_nombre(nombre_u, apellido_u)
                    
                    if not usuario_obj:
                        print("Usuario no encontrado.")
                        continue
                    
                    print("\nRoles disponibles:")
                    print("1. administrador")
                    print("2. usuario")
                    print("3. invitado")
                    
                    opcion_rol = input("Seleccione el número del rol: ").strip()
                    
                    match opcion_rol:
                        case "1":
                            nuevo_rol = Rol.ADMINISTRADOR
                        case "2":
                            nuevo_rol = Rol.USUARIO
                        case "3":
                            nuevo_rol = Rol.INVITADO
                        case _:
                            print("Opción de rol inválida.")
                            continue
                    
                    usuario_obj.set_rol(nuevo_rol)
                    usuario_dao.actualizar_rol_usuario(usuario_obj)
                    print(f"Rol actualizado correctamente a '{nuevo_rol.value}'.")
                        
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            case "6":
                print("Cerrando sesión...")
                break
                
            case _:
                print("Opción inválida.")


def main():
    while True:
        print("\n=== Sistema de Usuarios y Dispositivos ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("\nElija una opción: ").strip()
        
        match opcion:
            case "1":
                registrar_usuario()
                
            case "2":
                usuario = iniciar_sesion()
                if usuario:
                    match usuario.get_rol():
                        case Rol.ADMINISTRADOR:
                            menu_admin(usuario)
                        case _:
                            menu_usuario(usuario)
                            
            case "3":
                print("Saliendo del sistema...")
                sys.exit()
                
            case _:
                print("Opción inválida.")


if __name__ == "__main__":
    main()
