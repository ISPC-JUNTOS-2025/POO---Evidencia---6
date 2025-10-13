from dominio.usuario import Usuario
from enums.Rol import Rol
from dao.usuario_dao import UsuarioDao
from dao.dispositivo_dao import DispositivoDAO
from dominio.luz import Luz 
from dominio.aire_acondicionado import AireAcondicionado
from dominio.camara import Camara
from dominio.sensor_movimiento import SensorMovimiento
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
                            print(f"  Usuario ID: {d['id_usuario']}\n")
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
                            print(f"ID: {d['id_dispositivo']} - {d['nombre']} ({d['tipo_dispositivo']}) - {estado}")
                            print(f"  Usuario ID: {d['id_usuario']} | Marca: {d['marca']} | Modelo: {d['modelo']}")
                            print(f"  Consumo: {d['consumo_energetico']} W\n")
                    else:
                        print("\n✗ No hay dispositivos registrados.")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "2":
                try:
                    print("\n--- Crear dispositivo ---")
                    nombre = input("Nombre: ").strip()
                    marca = input("Marca: ").strip()
                    modelo = input("Modelo: ").strip()
                    consumo = float(input("Consumo energético (W): "))
                    id_usuario = usuario.get_id_usuario()  # Usar el ID del administrador logueado

                    print("\nTipos de dispositivo:")
                    print("1. Luz")
                    print("2. Aire Acondicionado")
                    print("3. Cámara")
                    print("4. Sensor de Movimiento")
                    
                    tipo = input("Seleccione tipo: ").strip()

                    match tipo:
                        case "1":
                            intensidad = int(input("Intensidad (0-100): "))
                            regulable = input("¿Es regulable? (s/n): ").lower() == "s"
                            
                            nuevo = Luz()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, intensidad, regulable)

                        case "2":
                            temperatura = int(input("Temperatura objetivo: "))
                            modo_eco = input("¿Modo eco? (s/n): ").lower() == "s"
                            
                            nuevo = AireAcondicionado()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, temperatura, modo_eco)

                        case "3":
                            print("Resoluciones: 720p, 1080p, 2K, 4K")
                            resolucion = input("Resolución: ").strip()
                            vision_nocturna = input("¿Visión nocturna? (s/n): ").lower() == "s"
                            
                            nuevo = Camara()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario, resolucion, vision_nocturna, True)

                        case "4":
                            nuevo = SensorMovimiento()
                            nuevo.crear_dispositivo(nombre, marca, modelo, consumo, id_usuario)
                            
                        case _:
                            print("✗ Tipo de dispositivo inválido.")
                            continue

                    dispositivo_dao.crear(nuevo)
                    print("✓ Dispositivo creado con éxito.")
                    
                except ValueError as e:
                    print(f"✗ Error en los datos ingresados: {e}")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "3":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    if dispositivos:
                        print("\n--- Dispositivos disponibles ---")
                        for d in dispositivos:
                            print(f"ID: {d['id_dispositivo']} - {d['nombre']} ({d['tipo_dispositivo']})")
                    
                    id_dispositivo = int(input("\nID del dispositivo a actualizar: "))
                    nombre = input("Nuevo nombre: ").strip()
                    marca = input("Nueva marca: ").strip()
                    modelo = input("Nuevo modelo: ").strip()
                    consumo = float(input("Nuevo consumo energético (W): "))
                    
                    dispositivo_actual = next((d for d in dispositivos if d['id_dispositivo'] == id_dispositivo), None)
                    
                    if dispositivo_actual:
                        tipo = dispositivo_actual['tipo_dispositivo']
                        
                        match tipo:
                            case "Luz":
                                d = Luz()
                                d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], 100, False)
                            case "Aire Acondicionado":
                                d = AireAcondicionado()
                                d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], 24, False)
                            case "Camara":
                                d = Camara()
                                d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'], "1080p", True, True)
                            case "Sensor de Movimiento":
                                d = SensorMovimiento()
                                d.crear_dispositivo(nombre, marca, modelo, consumo, dispositivo_actual['id_usuario'])
                            case _:
                                print("✗ Tipo de dispositivo no reconocido.")
                                continue
                        
                        d._id_dispositivo = id_dispositivo
                        
                        dispositivo_dao.actualizar(d)
                        print("✓ Dispositivo actualizado.")
                    else:
                        print("✗ Dispositivo no encontrado.")
                        
                except ValueError as e:
                    print(f"✗ Error en los datos: {e}")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "4":
                try:
                    dispositivos = dispositivo_dao.buscar_todos()
                    if dispositivos:
                        print("\n--- Dispositivos disponibles ---")
                        for d in dispositivos:
                            print(f"ID: {d['id_dispositivo']} - {d['nombre']} ({d['tipo_dispositivo']})")
                    
                    id_dispositivo = int(input("\nID del dispositivo a eliminar: "))
                    confirmacion = input(f"¿Está seguro de eliminar el dispositivo {id_dispositivo}? (s/n): ").lower()
                    
                    if confirmacion == 's':
                        if dispositivo_dao.eliminar(id_dispositivo):
                            print("✓ Dispositivo eliminado.")
                        else:
                            print("✗ No se encontró el dispositivo.")
                    else:
                        print("✗ Operación cancelada.")
                        
                except ValueError as e:
                    print(f"✗ Error: {e}")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "5":
                try:
                    usuarios = usuario_dao.buscar_usuarios()
                    print("\n--- Usuarios ---")
                    for u in usuarios:
                        print(f"ID: {u.get_id_usuario()} - {u.get_nombre()} {u.get_apellido()} ({u.get_rol().value})")

                    id_u = int(input("\nIngrese ID de usuario a cambiar rol: "))
                    
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
                            print("✗ Opción de rol inválida.")
                            continue
                    
                    usuario_obj = next((x for x in usuarios if x.get_id_usuario() == id_u), None)
                    if usuario_obj:
                        usuario_obj.set_rol(nuevo_rol)
                        usuario_dao.actualizar_rol_usuario(usuario_obj)
                        print(f"✓ Rol actualizado correctamente a '{nuevo_rol.value}'.")
                    else:
                        print("✗ Usuario no encontrado.")
                        
                except ValueError as e:
                    print(f"✗ Error: {e}")
                except Exception as e:
                    print(f"✗ Error: {e}")

            case "6":
                print("✓ Cerrando sesión...")
                break
                
            case _:
                print("✗ Opción inválida.")


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
                print("✓ Saliendo del sistema...")
                sys.exit()
                
            case _:
                print("✗ Opción inválida.")


if __name__ == "__main__":
    main()
