import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyfacebook import Api
from datetime import date
from datetime import datetime
import facebook
import pyfacebook
import tkinter as tk
from tkinter import filedialog

DATOS = Api(app_id = "692001264799472",app_secret = "60b272a45b500fef45f3c930d5d6d8df",long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",)
API_SDK = facebook.GraphAPI("EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD")
ID_PAGINA = "341526406956810"
CRUX = ChatBot("bot_10",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Disculpa, no logro entenderte. Intenta escribirlo de otra manera',
            'maximum_similarity_threshold': 0.90
        }])
LOG = open(r"C:\Users\Tomas\Documents\Tp Alg\TP2-Algoritmos\log.txt","w")

def entrenamiento_bot():
    '''
    PRE:
    Se entrenara al bot mediante las librerias de CHATTERBOT, se abre el archivo de entrenamiento "trainer.txt"
    y procede a entrenar al bot mediante cada linea, que pasaran a ser listas
    POST:
    Las respuestas seras guardadas dentro de una lista llamada "respuestas" con el fin de usarlas de frases clave
    para navegar dentro de las opciones del menu
    '''
    entrenamiento = ListTrainer(CRUX)
    texto = open(r"C:\Users\Tomas\Documents\Tp Alg\TP2-Algoritmos\trainer.txt")
    respuestas = []
    for linea in texto:
        linea = linea.rstrip("\n").split(",")
        entrenamiento.train(linea)
        if linea[-1] not in respuestas and len(respuestas) <= 8:
            respuestas.append(linea[-1])
    print(respuestas)
    texto.close()
    return respuestas

def opciones_bot(usuario):
    '''
    PRE:
    Se ingresara una vez sea solicitado este menu, es un printeo de las opciones las cuales se pueden realizar, para que
    el usuario pueda realizar las tareas que desee.
    POST:
    Se retira de la funcion sin ningun cambio y se reingresara en el caso que se vuelva a llamar las veces que sean falta.
    '''
    print('''
    -Dar Like
    -Leer posteos
    -Subir posteos y fotos
    -Actualizar post
    -Cantidad de seguidores
    -Actualizar datos del perfil
    -Salir          
          ''')
    return True

def like_posteo(post_id):
    '''
    PRE:
    Se ingresa mediante la funcion de "VER_POSTEOS" para con el ID enviado, se puede elegir el post a modificar.
    POST:
    Con el ID recibido se genera la peticion que va realizar el posteo del Like al posteo deseado, se volvera
    al menu previo, el cual es el de "VER_POSTEOS" para poder seguir realizando acciones.
    '''
    post_args = {"access_token":DATOS._access_token}
    peticion = DATOS._request(path="v9.0/{0}/likes".format(post_id),method="POST",post_args = post_args)

def ver_posteos(usuario, respuestas):
    '''
    PRE:
    Se ingresa mediante el menu de dialogo del BOT, desde aca se veran los posts y realizaran las modificaciones a los mismos.
    Se analiza el feed, cada publicacion individual y se evalua cuales son aptos para las modificaciones. Ya que solo los posteos,
    que no son modificaciones de perfil, son aptos para modificaciones.
    POST:
    Se envia los datos recolectados como el ID de cada publicacion, con el fin de poder realizar la modificacion. En este caso
    las modicaciones se enviaran a LIKE_POSTEO o ACTUALIZAR_POSTEO
    '''
    
    posts_id = []
    informacion_posts = DATOS.get_page_posts(page_id = ID_PAGINA,fields= "story,message,permalink_url",return_json = True,count=None)
    contador_posts = 1
    for informacion_post in informacion_posts:
        if ("story") not in informacion_post:        
            try:
                print("N°{0} Post.\n-{1}".format(contador_posts,informacion_post["message"]))
                post_id = (contador_posts,informacion_post["id"])
                posts_id.append(post_id)
                contador_posts += 1     
            except:
                print("N°{0} Post.\n-Imagen\n-Url: {1}".format(contador_posts,informacion_post["permalink_url"]))
                post_id = (contador_posts,informacion_post["id"])
                posts_id.append(post_id)
                contador_posts += 1 
    dicc_posts = dict(posts_id)
    finalizar_modificaciones = False
    while finalizar_modificaciones == False:        
        acciones_bot("seccion1")
        respuesta_usuario = input("{0}:".format(usuario)).upper()
        registro_log(respuesta_usuario,usuario)
        print(respuesta_usuario)
        if respuesta_usuario == "SI":
            eleccion_modificacion = True
            while eleccion_modificacion == True:
                    acciones_bot("seccion2")
                    numero_post_elegido = acciones_usuario(usuario)
                    try:
                        if numero_post_elegido.isnumeric and int(numero_post_elegido) < contador_posts:
                            eleccion_modificacion = False
                        else:
                            acciones_bot("seccion4")
                    except:
                        acciones_bot("seccion4")               
            finalizar_accion = False
            while finalizar_accion == False:
                acciones_bot("seccion5")
                selector_modificacion = mensajes(usuario)
                if str(selector_modificacion) == respuestas[2]:
                    like_posteo(dicc_posts[int(numero_post_elegido)])
                    acciones_bot("seccion6")
                    finalizar_accion = True 
                elif str(selector_modificacion) == respuestas[3]:
                    actualizar_post(dicc_posts[int(numero_post_elegido)])
                    acciones_bot("seccion6")
                    finalizar_accion = True                   
                else:
                    acciones_bot("seccion4")
        else:
            acciones_bot("seccion3")
            finalizar_modificaciones = True
            
    return True

def subir_posteo(usuario):
    '''
    PRE:
    Se ingresa mediante la conversacion con el bot, desde aca podremos realizar una creacion de post. Que sea unicamente 
    de texto, una foto o una foto con texto.
    POST:
    Se sube el posteo al feed de la PAGINA, y no se realizan mas cambios que ello. Se vuelve a la charla con el BOT.
    '''
    texto_post = input("Que queres que diga el post: ")
    post_args = {"message":texto_post,"access_token":DATOS._access_token}
    peticion = DATOS._request(path="v9.0/{0}/feed".format(ID_PAGINA),method="POST",post_args = post_args)
    print("Post creado con exito!")
    return True

def actualizar_post(post_id):
    '''
    PRE:
    Se adquiere el ID del post a actualizar mediante la funcion VER_POSTEOS. Se le ingresara un nuevo texto al posteo elegido
    
    '''
    modificacion_mensaje = input("Ingrese el nuevo texto del post: ")
    post_args = {"access_token":DATOS._access_token,"message":modificacion_mensaje}
    peticion = DATOS._request(path="v9.0/{0}".format(post_id,modificacion_mensaje),method="POST",post_args = post_args)

def cantidad_seguidores(usuario):
    '''
    Muestra la cantidad de seguidores,likes y nombre que tiene la pagina
    '''
    argumentos_get = {"fields" : "followers_count,fan_count,name"}
    peticion = DATOS._request(path="v9.0/{0}?".format(ID_PAGINA),args=argumentos_get,method="GET")
    data = DATOS._parse_response(peticion)
    print('''
          La cantidad de personas que interactuan con la pagina "{2}"
          son 
          {0} Followers 
          {1} Likes en la pagina
          '''.format(data["followers_count"],data["fan_count"],data["name"]))
    return True

def foto_archivo(page_id, usuario):
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()
    archivos_soportados = ["peg","bmp","png","gif","fif"]
    try:
        ingreso_correcto = False
        while not ingreso_correcto:
            filename = filedialog.askopenfilename()
            print(filename[-3::])
            if filename[-3::] in archivos_soportados:
                API_SDK.put_photo(image = open(r"{0}".format(filename),"rb"), album_path=f"{page_id}/picture")
                ingreso_correcto = True 
            else:
                acciones_bot("cod13")
                salir = acciones_usuario(usuario)
                if salir == "si":
                    ingreso_correcto = False
                else:
                    ingreso_correcto = True
    except:
            acciones_bot("cod14")

def foto_url(page_id, usuario):
    ingreso_correcto = False
    while not ingreso_correcto:
        try:
            url = acciones_usuario(usuario)
            post_args = {"picture":url,"access_token":DATOS._access_token}
            peticion = DATOS._request(path=f"v9.0/{page_id}/picture",method="POST",post_args = post_args)
            data = DATOS._parse_response(peticion)
            print(data)
            ingreso_correcto = True
        except pyfacebook.error.PyFacebookException as error:               
            if "(#100) picture should represent a valid URL" == error.message:
                acciones_bot("cod16")
            elif "Missing or invalid image file" == error.message:
                acciones_bot("cod17")
            else:
                acciones_bot("cod14")
                ingreso_correcto = True

def listar_fotos_publicadas(page_id, usuario):
    peticion = DATOS._request(path = f"v9.0/{page_id}/photos?type=uploaded", method = "GET")
    datos = DATOS._parse_response(peticion)
    lista_ids = [] 
    for ids in datos["data"]:
        lista_ids.append(ids["id"])
    for ids in lista_ids:
        peticion_2 = DATOS._request(path = f"v9.0/{ids}?fields=link,album", method = "GET")
        datos_2 = DATOS._parse_response(peticion_2)
        nro = lista_ids.index(ids) + 1
        print(nro, datos_2["link"], datos_2["album"]["name"])
    acciones_bot("cod18")        
    opcion = validacion_en_rango(1, len(lista_ids)+1,usuario)
    foto_seleccionada = lista_ids[opcion-1]
    return foto_seleccionada
        
def foto_ya_publicada(page_id, usuario):
    reuse = True
    foto = listar_fotos_publicadas(page_id,usuario)
    access_token = DATOS._access_token
    post_args = {"photo":foto, "access_token":access_token, "reuse":reuse}
    peticion = DATOS._request(path = f"v9.0/{page_id}/picture", method = "POST", post_args = post_args)
    acciones_bot("cod14")

def validacion_en_rango(rango_min, rango_max, usuario):
    opcion = acciones_usuario(usuario)
    while not opcion.isnumeric() or int(opcion) not in range(rango_min, rango_max):
        acciones_bot("cod2")
        opcion = acciones_usuario(usuario)
    return int(opcion)

def cambiar_foto_perfil(usuario, page_id):
    acciones_bot("cod10")
    print("1. Subir una nueva foto de perfil\n2. Seleccionar una ya publicada")
    opcion = validacion_en_rango(1,3,usuario)
    if opcion == 1:
        acciones_bot("cod11")
        print("1. Seleccionar archivo\n2. mediante URL")
        opcion_2 = validacion_en_rango(1,3,usuario)
        if opcion_2 == 1:
            acciones_bot("cod12")
            foto_archivo(page_id,usuario)
        if opcion_2 == 2:
            acciones_bot("cod15")
            foto_url(page_id, usuario)
    if opcion == 2:
        foto_ya_publicada(page_id, usuario)
    return True

def actualizar_datos(usuario):
    '''
    Actualiza los datos de la pagina
    '''
    cambios = {
        1:("Descripcion de pagina","about"),
        2:("Email","emails"),   
        3:("Telefono","phone"),
        4:("Foto de perfil","")
        }
    finalizar = False
    continuar = False
    while not finalizar:
        acciones_bot("cod1")
        for codigo, valor in cambios.items():
            print(f"{codigo}. {valor[0]}")
        opcion = acciones_usuario(usuario)
        contador = 0
        while not opcion.isnumeric() or int(opcion) not in range(1,5):
            acciones_bot("cod2")
            opcion = acciones_usuario(usuario)
        opcion = int(opcion) 
        if opcion == 1:
            acciones_bot("cod3")
        elif opcion == 2:
            acciones_bot("cod4")
        elif opcion == 3:
            acciones_bot("cod5")
        elif opcion == 4:
            acciones_bot("cod9")
            cambiar_foto_perfil(usuario,"341526406956810")
            continuar = True
            
        while continuar == False:
            try:
                cambio = input(f"Ingrese su nuevo/a {cambios[opcion][0]}: ".capitalize())
                registro_log(cambio,usuario)
                if opcion == 2:
                    cambio = cambio.split()
                post_args = {"Access token":DATOS._access_token}
                peticion = DATOS._request(path = f"v9.0/{ID_PAGINA}?{cambios[opcion][1]}={cambio}", method = "POST", post_args = post_args)
                data = DATOS._parse_response(peticion)
                acciones_bot("cod8")
                continuar = True 
            except:
                if opcion == 2:
                    acciones_bot("cod6")
                else:
                    acciones_bot("cod7")
        
        finalizar = True
    return True

def subir_foto(usuario):
    '''
    Hay que ver si se junta junto con la funcion SUBIR_POSTEO
    '''
    print("Subir Foto")
    return True

def finalizar(usuario):
    '''
    Opcion ingresada mediante el chat de bot
    POST:
    Finaliza la charla con el bot y tambien finaliza la ejecucion del programa
    '''
    return False

def conversacion(usuario,respuestas_clave):
    '''
    PRE:
    Toma el nombre del usuario y las respuestas previamente guardadas del entrenamiento de crux en ENTRENAMIENTO_BOT.
    Se generara una charla con el nombre del usuario y del bot.
    POST:
    Se redirecciona a las distintas funciones y a medida que ocurre se generan los cambios en el LOG. La charla
    continua hasta que el usuario decida Finalizarla mediante la conversacion con el bot
    '''
    opciones = {0:opciones_bot,
                1:ver_posteos,                
                4:subir_posteo,
                5:subir_foto,
                6:cantidad_seguidores,
                7:actualizar_datos,
                8:finalizar
                }
    acciones_bot("saludo inicial")
    continuar = True
    while continuar == True:        
        respuesta_bot = mensajes(usuario)
        if str(respuesta_bot) in respuestas_clave:
            indice_respuesta = respuestas_clave.index(str(respuesta_bot))
            if indice_respuesta is 1:
                continuar = opciones[indice_respuesta](usuario,respuestas_clave)
            else:
                continuar = opciones[indice_respuesta](usuario)

def registro_log (dialogo,usuario):
    hora_actual = datetime.now()
    dialogo_log = str("{} {}:{}:{} {} : {}".format(date.today(),hora_actual.hour,hora_actual.minute,hora_actual.second,usuario,dialogo))
    LOG.write(dialogo_log+"\n")

def mensajes(usuario):
    peticion = input("{0}:".format(usuario))
    registro_log(peticion,usuario)
    peticion = peticion.lower()
    respuesta_bot = CRUX.get_response(peticion)
    registro_log(respuesta_bot,"Crux")
    print("Crux:{0}".format(respuesta_bot))
    return respuesta_bot

def acciones_bot(codigo_accion):
    lectura_accion = CRUX.get_response(codigo_accion)
    print("Crux: {0}".format(lectura_accion))
    registro_log(lectura_accion,"Crux")

def acciones_usuario(usuario):
    accion_usuario = input("{0}: ".format(usuario))
    registro_log(accion_usuario,usuario)
    return accion_usuario
    
def main():
    entrenamiento = entrenamiento_bot()
    usuario = input("Ingrese su nombre: ")
    charla = conversacion(usuario,entrenamiento)
    LOG.close()
    print("FIN")
    
main()