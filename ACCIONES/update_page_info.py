from pyfacebook import Api
import json

api = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )

cambios = {
        1:("descripcion de pagina","about"),
        2:("email","emails"),   
        3:("telefono","phone")
        }


def validacion_en_rango(rango_min, rango_max):
    opcion = input("Opcion: ")
    while not opcion.isnumeric() or int(opcion) not in range(rango_min, rango_max):
        opcion = input("La opcion ingresada no es valida. Por favor, vuelva a intentar: ")
    return int(opcion)


def cambio(page_id):
    print("Que desea modificar del perfil:")
    for codigo, valor in cambios.items():
        print(f"{codigo}. {valor[0]}")
    opcion = input("Opcion: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,4):
        opcion = input("La opcion ingresada no es valida. Por favor, vuelva a intentar: ")
    opcion = int(opcion) 
    continuar = False
    while continuar == False:
        try:
            peticion_2 = api._request(path = f"v9.0/{page_id}?fields={cambios[opcion][1]}", method = "GET")
            data_2 = api._parse_response(peticion_2)
            print(f"Su {cambios[opcion][0]} actual es: {data_2[cambios[opcion][1]]}")
            cambio = input(f"Ingrese su nuevo/a {cambios[opcion][0]}: ".capitalize())
            if opcion == 2:
                cambio = cambio.split()
            post_args = {"Access token":api._access_token}
            peticion = api._request(path = f"v9.0/{page_id}?{cambios[opcion][1]}={cambio}", method = "POST")
            data = api._parse_response(peticion)
            continuar = True 
        except:
            if opcion == 2:
                print("Debe ingresar un email valido.")
            else:
                print("Debe ingresar un numero de telefono valido.")
    print("Se modificaron los datos con exito!")

data = cambio("341526406956810")

print(data)





            try:
                peticion_2 = DATOS._request(f"v9.0/{ID_PAGINA}?fields={cambios[opcion][1]}", method = "GET")
                data_2 = DATOS._parse_response(peticion_2)
                print(f"Su {cambios[opcion][0]} actual es: {data_2[cambios[opcion][1]]}")
                cambio = input(f"Ingrese su nuevo/a {cambios[opcion][0]}: ".capitalize())
                registro_log(cambio,usuario)
                if opcion == 2:
                    cambio = cambio.split()
                post_args = {"Access token":DATOS._access_token}
                peticion = DATOS._request(
                    path = f"v9.0/{ID_PAGINA}?{cambios[opcion][1]}={cambio}",
                    method = "POST",
                    post_args = post_args)
                data = DATOS._parse_response(peticion)
                acciones_bot("cod8")
                continuar = True
            except:
                if opcion == 2:
                    acciones_bot("cod6")
                else:
                    acciones_bot("cod7")
        acciones_bot("cod19")
        decision = acciones_usuario(usuario)
        if decision == "si":
            finalizar = False
        else:
            finalizar = True