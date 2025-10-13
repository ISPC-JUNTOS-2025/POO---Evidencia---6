sustitucion_de_caracteres = {
    'a': '@',
    'e': '#',
    'i': '$',
    'o': '%',
    'u': '&',
    'A': '!',
    'E': '^',
    'I': '*',
    'O': '(',
    'U': ')',
    '1': '+',
    '2': '-',
    '3': '=',
    '4': '¿',
    '5': '¡',
    '7': '´',
    '8': '}',
    '9': ']'
}

def verificar_email(email):
    lista_dominios = ("@gmail.com", "@outlook.com")
    email = email.strip()
    email_dividido = email.split("@")
    if len(email_dividido) != 2 or not email_dividido[0] or not email_dividido[1]:
        raise ValueError(f"Formato de email inválido. Asegúrese de que haya un nombre de usuario y un dominio. Formatos válidos: {lista_dominios}")
    dominio_con_arroba = "@" + email_dividido[1]
    if dominio_con_arroba not in lista_dominios:
        raise ValueError(f"El email debe contener un '@'. Formatos válidos: {lista_dominios}")

def encriptar_contraseña(contraseña):
    texto_encriptado = ""
    for caracter in contraseña:
        if caracter in sustitucion_de_caracteres:
            texto_encriptado += sustitucion_de_caracteres[caracter]
        else:
            texto_encriptado += caracter
    return texto_encriptado

def desencriptar_contraseña(contraseña_encriptada):
    contraseña_desencriptada = ""
    sustitucion_de_caracteres_inverso = {valor: clave for clave, valor in sustitucion_de_caracteres.items()}
    for caracter in contraseña_encriptada:
        if caracter in sustitucion_de_caracteres_inverso:
            contraseña_desencriptada += sustitucion_de_caracteres_inverso[caracter]
        else:
            contraseña_desencriptada += caracter
    return contraseña_desencriptada