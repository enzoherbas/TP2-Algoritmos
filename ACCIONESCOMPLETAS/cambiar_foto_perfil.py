import facebook
import pyfacebook
import tkinter as tk
from tkinter import filedialog
from pyfacebook import Api
import json

window = tk.Tk()
window.wm_attributes('-topmost', 1)
window.withdraw()

api = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )
long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
api_2 = facebook.GraphAPI(long_term_token)

def foto_archivo(page_id):
        archivos_soportados = ["peg","bmp","png","gif","iff"]
        try: 
                ingreso_correcto = False
                while not ingreso_correcto:
                        filename = filedialog.askopenfilename()
                        if filename[-3::] in archivos_soportados:
                                ingreso_correcto = True
                        else:
                                print("El archivo elegido es incorrecto, vuelva a elegir.")

                api_2.put_photo(image = open(r"{0}".format(filename),"rb"), album_path=f"{page_id}/picture")             
        except:
                print("La foto de perfil ha sido actualizada.")                

def foto_url(page_id):
                ingreso_correcto = False
                while not ingreso_correcto:
                        try:
                                url = input("Ingrese url de la imagen: ")
                                post_args = {"picture":url,"access_token":api._access_token}
                                peticion = api._request(path=f"v9.0/{page_id}/picture",method="POST",post_args = post_args)
                                data = api._parse_response(peticion)
                                print(data)
                                ingreso_correcto = True
                        except pyfacebook.error.PyFacebookException as error:
                                        if "(#100) picture should represent a valid URL" == error.message:
                                                print("URL ingresado no valido.")
                                        elif "Missing or invalid image file" == error.message:
                                                print("URL ingresado no contiene una imagen.")
                                        else:
                                                print("Se ha subio la foto correctamente.")
                                                ingreso_correcto = True
                                



def listar_fotos_publicadas(page_id):
        peticion = api._request(path = f"v9.0/{page_id}/photos?type=uploaded", method = "GET")
        datos = api._parse_response(peticion)
        lista_ids = [] 
        for ids in datos["data"]:
                lista_ids.append(ids["id"])
        for ids in lista_ids:
                peticion_2 = api._request(path = f"v9.0/{ids}?fields=link,album", method = "GET")
                datos_2 = api._parse_response(peticion_2)
                nro = lista_ids.index(ids) + 1
                print(nro, datos_2["link"], datos_2["album"]["name"])
        opcion = validacion_en_rango(1, len(lista_ids)+1)
        foto_seleccionada = lista_ids[opcion-1]
        return foto_seleccionada
        
def foto_ya_publicada(page_id):
        reuse = True
        foto = listar_fotos_publicadas(page_id)
        access_token = api._access_token
        post_args = {"photo":foto, "access_token":access_token, "reuse":reuse}
        peticion = api._request(path = f"v9.0/{page_id}/picture", method = "POST", post_args = post_args)
        print("Se ha cambiado la foto de perfil")

def validacion_en_rango(rango_min, rango_max):
    opcion = input("Opcion: ")
    while not opcion.isnumeric() or int(opcion) not in range(rango_min, rango_max):
        opcion = input("La opcion ingresada no es valida. Por favor, vuelva a intentar: ")
    return int(opcion)

def eleccion(page_id):
        print("""Elija una opcion:
        1. Subir una nueva foto de perfil
        2. Seleccionar una ya publicada """)
        opcion = validacion_en_rango(1,3)
        if opcion == 1:
                print("""Elija una opcion:
        1. Seleccionar archivo
        2. Mediante URL """)
                opcion_2 = validacion_en_rango(1,3)
                if opcion_2 == 1:
                        foto_archivo(page_id)
                if opcion_2 == 2:
                        foto_url(page_id)
        if opcion == 2:
                foto_ya_publicada(page_id)
                        
def main():
        page_id = "341526406956810"
        eleccion(page_id)
main()