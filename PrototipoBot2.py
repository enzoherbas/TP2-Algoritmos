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
from colorama import init, Fore, Back, Style
import requests


ID_PAGINA = "341526406956810"


def entrenamiento_bot(crux_bot):
    entrenamiento = ListTrainer(crux_bot, show_training_progress=False)
    texto_entrenamiento = open(r"C:\Users\Tomas\Documents\Tp Alg\TP2-Algoritmos\trainer.txt", "r")
    respuestas_clave = []
    for linea_de_dialogo in texto_entrenamiento:
        linea_de_dialogo = linea_de_dialogo.rstrip("\n").split(",")
        entrenamiento.train(linea_de_dialogo)
        if len(respuestas_clave) <= 9:
            respuestas_clave.append(linea_de_dialogo[-1])
    texto_entrenamiento.close()
    return respuestas_clave


def like_posteo(post_id, datos_usuario):
    '''
    PRE:
    Se ingresa mediante la funcion de "modificacion_post" para con el ID
    enviado,
    se puede elegir el
    post a modificar. Con el ID recibido se genera la peticion que va realizar
    el posteo del Like al posteo deseado.
    POST:
    No devuelve nada, desde aca se genera toda la peticion necesaria.
    '''
    post_args = {"access_token": datos_usuario._access_token}
    peticion = datos_usuario._request(
        path="v9.0/{0}/likes".format(post_id),
        method="POST",
        post_args=post_args)


def ver_posteos(usuario, respuestas, datos_usuario, crux_bot, log):
    '''
    PRE:
    Se ingresa mediante el menu de dialogo del BOT, desde aca se veran los
    posts y realizaran las modificaciones a los mismos.Se analiza el feed,
    cada publicacion individual y se evalua cuales son aptos para las
    modificaciones. Ya que solo los posteos,que no son modificaciones de
    perfil, son aptos para modificaciones.
    POST:
    Se envia los datos recolectados como el ID de cada publicacion,
    con el fin de poder realizar la modificacion.
    En este caso las modicaciones se enviaran a"modificacion_posts"
    para seguir con las ordenes de modificacion
    '''
    dicc_posts, cantidad_post = visualizar_post(datos_usuario)
    acciones_bot("seccion1", crux_bot, log)
    respuesta_usuario = acciones_usuario(usuario, log)
    while respuesta_usuario == "si":
        modificacion_posts(
            dicc_posts,
            usuario,
            cantidad_post,
            respuestas,
            datos_usuario,
            crux_bot,
            log)
        acciones_bot("seccion11", crux_bot, log)
        continuar_modificaciones = acciones_usuario(usuario, log)
        if continuar_modificaciones == "si":
            dicc_posts, cantidad_post = visualizar_post(datos_usuario)
        else:
            respuesta_usuario = False


def visualizar_post(datos_usuario):
    posts_id = []
    informacion_posts = datos_usuario.get_page_posts(
        page_id=ID_PAGINA,
        fields="story,message,permalink_url,created_time",
        return_json=True,
        count=None)
    cantidad_post = 1
    for informacion_post in informacion_posts:
        fecha_post = informacion_post["created_time"].split("T")
        if ("story") not in informacion_post:
            if ("message") in informacion_post:
                print('''
                        PUBLICACION N°{0}                 {1}
                        ////////////////////////////////////////////
                        Texto del Post:{2}'''.format(
                            cantidad_post,
                            fecha_post[0],
                            informacion_post["message"]))
                post_id = (cantidad_post, informacion_post["id"])
                posts_id.append(post_id)
                cantidad_post += 1
            else:
                print('''
                        PUBLICACION N°{0}                  {1}
                        ////////////////////////////////////////////
                        El POST es una imagen!
                        -URL de imagen: {2}'''.format(
                            cantidad_post,
                            fecha_post[0],
                            informacion_post["permalink_url"]))
                post_id = (cantidad_post, informacion_post["id"])
                posts_id.append(post_id)
                cantidad_post += 1
    return dict(posts_id), cantidad_post


def subir_posteo(usuario, datos_usuario, crux_bot, log):
    '''
    PRE:
    Se ingresa mediante la conversacion con el bot, desde aca podremos realizar
    una creacion de post. Que sea unicamente de texto.
    POST:
    Se sube el posteo al feed de la PAGINA, y no se realizan
    mas cambios que ello.
    Se vuelve a la charla con el BOT.
    '''
    acciones_bot("seccion7", crux_bot, log)
    texto_post = acciones_usuario(usuario, log)
    post_args = {
        "message": texto_post,
        "access_token": datos_usuario._access_token}
    peticion = datos_usuario._request(
        path="v9.0/{0}/feed".format(ID_PAGINA),
        method="POST",
        post_args=post_args)
    acciones_bot("seccion8", crux_bot, log)


def actualizar_post(post_id, datos_usuario):
    '''
    PRE:
    Se adquiere el ID del post a actualizar mediante la funcion
    "modifacion_posts". Se le ingresara un nuevo texto al posteo elegido
    '''
    modificacion_mensaje = input("Ingrese el nuevo texto del post: ")
    post_args = {
        "access_token": datos_usuario._access_token,
        "message": modificacion_mensaje}
    peticion = datos_usuario._request(
        path="v9.0/{0}".format(post_id, modificacion_mensaje),
        method="POST",
        post_args=post_args)


def eliminar_post(post_id, datos_usuario):
    '''
    PRE: Se abre desde la funcion "modificacion_posts", para poder eliminar
         el post seleccionado.
    '''
    args = {"method": "delete", "access_token": datos_usuario._access_token}
    peticion = datos_usuario._request(
        path="v9.0/{0}".format(post_id),
        post_args=args,
        method="POST")
    data = datos_usuario._parse_response(peticion)


def modificacion_posts(id_posts, usuario, cantidad_post, respuestas, datos_usuario, crux_bot, log):
    '''
    PRE: Se ingresan los id_posts para poder realizar la modificacion
    deseada mediante la charlacon el bot y una parte con el sistema para
    evitar errores con la palabra de afirmacion. lacantidad de posts tambien
    para corroborar que la eleccion de post a modificar este dentro de los
    rangos de eleccion, las "respuestas" ingresan con el fin de corroborar que
    la respuesta del bot sea la deseada e ingrese a las funciones "like_post",
    "actualizar_post" o "eliminar_post"
    POST: Retora a la opcion anterior de "VER_POSTEOS" para verificar si desea
    seguir con las modificaciones.
    '''
    acciones_bot("seccion2", crux_bot, log)
    numero_post_elegido = acciones_usuario(usuario, log)
    if numero_post_elegido.isnumeric():
        if int(numero_post_elegido) < cantidad_post:
            eleccion_modificacion = False
    else:
        acciones_bot("seccion4", crux_bot, log)
    finalizar_accion = False
    while not finalizar_accion:
        acciones_bot("seccion5", crux_bot, log)
        selector_modificacion = mensajes(usuario, crux_bot, log)
        if str(selector_modificacion) == respuestas[7]:
            like_posteo(id_posts[int(numero_post_elegido)], datos_usuario)
            acciones_bot("seccion6", crux_bot, log)
            finalizar_accion = True
        elif str(selector_modificacion) == respuestas[8]:
            actualizar_post(id_posts[int(numero_post_elegido)], datos_usuario)
            acciones_bot("seccion6", crux_bot, log)
            finalizar_accion = True
        elif str(selector_modificacion) == respuestas[9]:
            eliminar_post(id_posts[int(numero_post_elegido)], datos_usuario)
            acciones_bot("seccion6", crux_bot, log)
            finalizar_accion = True
        else:
            acciones_bot("seccion4", crux_bot, log)


def cantidad_seguidores(usuario, datos_usuario, log):
    '''
    PRE:
    Muestra la cantidad de seguidores,likes y nombre que tiene la pagina
    '''
    argumentos_get = {"fields": "followers_count,fan_count,name"}
    peticion = datos_usuario._request(
        path="v9.0/{0}?".format(ID_PAGINA),
        args=argumentos_get,
        method="GET")
    data = datos_usuario._parse_response(peticion)
    estadisticas_pagina = ('''
          La cantidad de personas que interactuan con la pagina "{2}"
          son
          {0} Followers
          {1} Likes en la pagina
          '''.format(data["followers_count"], data["fan_count"], data["name"]))
    print("Crux: {}".format(estadisticas_pagina))
    registro_log(estadisticas_pagina, "Crux", log)


def foto_archivo(usuario, accion, datos_api_sdk, crux_bot, log):
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()
    archivos_soportados = ["peg", "bmp", "png", "gif", "fif"]
    try:
        ingreso_correcto = False
        while not ingreso_correcto:
            filename = filedialog.askopenfilename()
            if filename[-3::] in archivos_soportados:
                if accion is True:
                    datos_api_sdk.put_photo(image=open(r"{0}".format(filename), "rb"), album_path=f"{ID_PAGINA}/picture")
                    ingreso_correcto = True
                elif not accion:
                    acciones_bot("cod22", crux_bot, log)
                    datos_api_sdk.put_photo(image=open(r"{0}".format(filename), "rb"), message=acciones_usuario(usuario, log))
                    ingreso_correcto = True
            else:
                acciones_bot("cod13", crux_bot, log)
                salir = acciones_usuario(usuario, log)
                if salir == "si":
                    ingreso_correcto = False
                else:
                    ingreso_correcto = True
    except:
        acciones_bot("cod14", crux_bot, log)


def foto_url(usuario, accion, datos_usuario, crux_bot, log):
    ingreso_correcto = False
    while not ingreso_correcto:
        try:
            acciones_bot("cod23", crux_bot, log)
            url = acciones_usuario(usuario, log)
            if accion is True:
                post_args = {
                    "picture": url,
                    "access_token": datos_usuario._access_token}
                peticion = datos_usuario._request(
                    path=f"v9.0/{ID_PAGINA}/picture",
                    method="POST",
                    post_args=post_args)
                data = datos_usuario._parse_response(peticion)
                print(data)
                ingreso_correcto = True
            if not accion:
                acciones_bot("cod22", crux_bot, log)
                mensaje = acciones_usuario(usuario, log)
                post_args = {
                    "url": url,
                    "access_token": datos_usuario._access_token,
                    "caption": mensaje}
                peticion = datos_usuario._request(
                    path=f"v9.0/{ID_PAGINA}/photos",
                    method="POST",
                    post_args=post_args)
                data = datos_usuario._parse_response(peticion)
                ingreso_correcto = True
        except pyfacebook.error.PyFacebookException as error:
            if ("(#100) picture should represent a valid URL" == error.message) or ("(#100) url should represent a valid URL" == error.message):
                acciones_bot("cod16", crux_bot, log)
            elif ("Missing or invalid image file" == error.message) or ("Invalid parameter" == error.message) or ("Could not fetch picture" == error.message):
                acciones_bot("cod17", crux_bot, log)
            else:
                acciones_bot("cod14", crux_bot, log)
                ingreso_correcto = True


def listar_fotos_publicadas(usuario, datos_usuario, crux_bot, log):
    peticion = datos_usuario._request(
        path=f"v9.0/{ID_PAGINA}/photos?type=uploaded",
        method="GET")
    datos = datos_usuario._parse_response(peticion)
    lista_ids = []
    for ids in datos["data"]:
        lista_ids.append(ids["id"])
    for ids in lista_ids:
        peticion_2 = datos_usuario._request(
            path=f"v9.0/{ids}?fields=link,album",
            method="GET")
        datos_2 = datos_usuario._parse_response(peticion_2)
        nro = lista_ids.index(ids) + 1
        print(nro, datos_2["link"], datos_2["album"]["name"])
    acciones_bot("cod18", crux_bot, log)
    opcion = validacion_en_rango(1, len(lista_ids)+1, usuario, crux_bot, log)
    foto_seleccionada = lista_ids[opcion-1]
    return foto_seleccionada


def foto_ya_publicada(usuario, datos_usuario, crux_bot, log):
    reuse = True
    foto = listar_fotos_publicadas(usuario, datos_usuario, crux_bot, log)
    access_token = datos_usuario._access_token
    post_args = {"photo": foto, "access_token": access_token, "reuse": reuse}
    peticion = datos_usuario._request(
        path=f"v9.0/{ID_PAGINA}/picture",
        method="POST",
        post_args=post_args)
    acciones_bot("cod14", crux_bot, log)


def validacion_en_rango(rango_min, rango_max, usuario, crux_bot, log):
    opcion = acciones_usuario(usuario, log)
    while not opcion.isnumeric() or int(opcion) not in range(rango_min, rango_max):
        acciones_bot("cod2", crux_bot, log)
        opcion = acciones_usuario(usuario, log)
    return int(opcion)


def cambiar_foto_perfil(usuario, datos_api_sdk, datos_usuario, crux_bot, log):

    acciones_bot("cod10", crux_bot, log)
    print("1. Subir una nueva foto de perfil\n2. Seleccionar una ya publicada")
    opcion = validacion_en_rango(1, 3, usuario, crux_bot, log)
    if opcion == 1:
        acciones_bot("cod11", crux_bot, log)
        print("1. Seleccionar archivo\n2. mediante URL")
        opcion_2 = validacion_en_rango(1, 3, usuario, crux_bot, log)
        if opcion_2 == 1:
            acciones_bot("cod12", crux_bot, log)
            foto_archivo(usuario, True, datos_api_sdk, crux_bot, log)
        if opcion_2 == 2:
            foto_url(usuario, True, datos_usuario, crux_bot, log)
    if opcion == 2:
        foto_ya_publicada(usuario, datos_usuario, crux_bot, log)


def actualizar_datos(usuario, datos_api_sdk, datos_usuario, crux_bot, log):
    '''
    Actualiza los datos de la pagina
    '''
    cambios = {
        1: ("Descripcion de pagina", "about"),
        2: ("Email", "emails"),
        3: ("Telefono", "phone"),
        4: ("Foto de perfil", None)
        }
    finalizar = False
    continuar = False
    while not finalizar:
        acciones_bot("cod1", crux_bot, log)
        for codigo, valor in cambios.items():
            print(f"{codigo}. {valor[0]}")
        opcion = acciones_usuario(usuario, log)
        contador = 0
        while not opcion.isnumeric() or int(opcion) not in range(1, 5):
            acciones_bot("cod2", crux_bot, log)
            opcion = acciones_usuario(usuario, log)
        opcion = int(opcion)
        if opcion == 1:
            acciones_bot("cod3", crux_bot, log)
        elif opcion == 2:
            acciones_bot("cod4", crux_bot, log)
        elif opcion == 3:
            acciones_bot("cod5", crux_bot, log)
        elif opcion == 4:
            acciones_bot("cod9", crux_bot, log)
            cambiar_foto_perfil(
                usuario,
                datos_api_sdk,
                datos_usuario,
                crux_bot,
                log)
            continuar = True

        while not continuar:
            try:
                peticion_2 = datos_usuario._request(
                    f"v9.0/{ID_PAGINA}?fields={cambios[opcion][1]}",
                    method="GET")
                data_2 = datos_usuario._parse_response(peticion_2)
                print(f"Su {cambios[opcion][0]} actual es: {data_2[cambios[opcion][1]]}")
                cambio = input(f"Ingrese su nuevo/a {cambios[opcion][0]}: ".capitalize())
                registro_log(cambio, usuario, log)
                if opcion == 2:
                    cambio = cambio.split()
                post_args = {"Access token": datos_usuario._access_token}
                peticion = datos_usuario._request(
                    path=f"v9.0/{ID_PAGINA}?{cambios[opcion][1]}={cambio}",
                    method="POST",
                    post_args=post_args)
                data = datos_usuario._parse_response(peticion)
                acciones_bot("cod8", crux_bot, log)
                continuar = True
            except:
                if opcion == 2:
                    acciones_bot("cod6", crux_bot, log)
                else:
                    acciones_bot("cod7", crux_bot, log)
        acciones_bot("cod19", crux_bot, log)
        decision = acciones_usuario(usuario, log)
        if decision == "si":
            finalizar = False
            continuar = False
        else:
            finalizar = True
            acciones_bot("cod20", crux_bot, log)


def subir_foto(usuario, datos_api_sdk, datos_usuario, crux_bot, log):

    acciones_bot("cod21", crux_bot, log)
    print("1. Seleccionando archivo\n2. Mediante URL")
    opcion = validacion_en_rango(1, 3, usuario, crux_bot, log)
    if opcion == 1:
        foto_archivo(usuario, False, datos_api_sdk, crux_bot, log)
    if opcion == 2:
        foto_url(usuario, False, datos_usuario, crux_bot, log)
    acciones_bot("cod14", crux_bot, log)
    acciones_bot("cod20", crux_bot, log)


def conversacion(usuario, datos_api, datos_api_sdk, crux_bot, respuestas_clave, log):
    '''
    PRE:
    Toma el nombre del usuario y las respuestas previamente guardadas del
    entrenamiento de crux en ENTRENAMIENTO_BOT. Se generara una charla con
    el nombre del usuario y del bot.
    POST:
    Se redirecciona a las distintas funciones y a medida que ocurre se generan
    los cambiosm en el LOG. La charla continua hasta que el usuario decida
    Finalizarla mediante la conversacion con el bot
    '''
    acciones_bot("saludo inicial", crux_bot, log)
    continuar = True
    while continuar is True:
        respuesta_bot = mensajes(usuario, crux_bot, log)
        if str(respuesta_bot) in respuestas_clave:
            indice_respuesta = respuestas_clave.index(str(respuesta_bot))
            if indice_respuesta == 6:
                print("Crux: Hasta luego, {}.".format(usuario))
                continuar = False
            else:
                selector_funciones(
                    indice_respuesta,
                    usuario,
                    datos_api,
                    datos_api_sdk,
                    crux_bot,
                    respuestas_clave,
                    log)


def selector_funciones(indice_respuesta, usuario, datos_api, datos_api_sdk, crux_bot, respuestas_clave, log):
    if indice_respuesta == 0:
        print('''
    -Ver posteos y modificarlos
    -Subir foto
    -Subir posteo
    -Cantidad de seguidores
    -Actualizar datos del perfil
    -Salir
    ''')
    elif indice_respuesta == 1:
        ver_posteos(usuario, respuestas_clave, datos_api, crux_bot, log)
    elif indice_respuesta == 2:
        subir_posteo(usuario, datos_api, crux_bot, log)
    elif indice_respuesta == 3:
        subir_foto(usuario, datos_api_sdk, datos_api, crux_bot, log)
    elif indice_respuesta == 4:
        cantidad_seguidores(usuario, datos_api, log)
    elif indice_respuesta == 5:
        actualizar_datos(usuario, datos_api_sdk, datos_api, crux_bot, log)


def registro_log(dialogo, usuario, log):
    '''
    PRE:
    Ingresa el dialogo junto al usuario para poder ingresarlo al log en forma
    de dialogo con el dia y hora del momento del mensaje.
    POST:
    Devuelve el archivo LOG con las nuevas modificaciones.
    '''
    hora_actual = datetime.now()
    dialogo_log = str("{0} {1}:{2}:{3} {4} : {5}".format(
        date.today(),
        hora_actual.hour,
        hora_actual.minute,
        hora_actual.second,
        usuario,
        dialogo))
    log.write(dialogo_log+"\n")


def mensajes(usuario, crux_bot, log):
    '''
    PRE:
    Se ingresan los datos del usuario para poder registrarlo en el LOG, se
    genera una conversacion de respuesta con el bot
    POST:
    El bot devuelve una respuesta, que abrira o no una funcion con respecto en
    donde se use. Se comparara esa respuesta en la lista de palabras claves
    para ver si esta en ellas esa respuesta otorgada.
    '''
    peticion = input("{0}:".format(usuario))
    registro_log(peticion, usuario, log)
    if not peticion or peticion.isspace():
        respuesta_bot = crux_bot.get_response("cod24")
        print(f"Crux: {respuesta_bot}")
        registro_log(respuesta_bot, "Crux", log)
    else:
        peticion = peticion.lower()
        respuesta_bot = crux_bot.get_response(peticion)
        registro_log(respuesta_bot, "Crux", log)
        print("Crux:{0}".format(respuesta_bot))
    return respuesta_bot


def acciones_bot(codigo_accion, crux_bot, log):
    '''
    PRE:
    Se ingresa un "codigo_accion" que no es mas que una cadena de texto que
    esta diseñada para poder abrir una funcion en especifico, se utilizara a
    lo largo del programa
    POST:
    Printea la respuesta del bot con respecto a ese "codigo_accion" y se
    guardara en el LOG
    '''
    lectura_accion = crux_bot.get_response(codigo_accion)
    print("Crux: {0}".format(lectura_accion))
    registro_log(lectura_accion, "Crux", log)


def acciones_usuario(usuario, log):
    '''
    PRE:
    Se ingresa el usuario para generar un dialogo del USUARIO en distintas
    instancias del funcionamiento del programa.
    POST:
    Retorna esa accion del usuario que sera leida por el bot y generara una
    respuesta tambien el dialogo se guardara en el LOG
    '''
    accion_usuario = input("{0}: ".format(usuario))
    registro_log(accion_usuario, usuario, log)
    return accion_usuario.lower()


def verificar_conexion():
    try:
        r = requests.head("http://facebook.com", timeout=3)
        return True

    except requests.ConnectionError as error:
        return False


def datos():
    nombre_usuario = input("Por favor, ingrese su usuario: ")
    datos_api = Api(app_id="692001264799472", app_secret="60b272a45b500fef45f3c930d5d6d8df", long_term_token="EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",)
    datos_api_sdk = facebook.GraphAPI("EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD")
    crux_bot = ChatBot("CRUX", logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Disculpa, no logro entenderte. Intenta escribirlo de otra manera',
            'maximum_similarity_threshold': 0.30
        }])
    log = open("log.txt", "a")
    log.write("\nNueva sesion\nFecha, hora, Usuario/Crux, Mensaje\n")
    conexion = verificar_conexion()

    return nombre_usuario, datos_api, datos_api_sdk, crux_bot, log, conexion


def informacion_inicial():
    print(Fore.BLACK +
    '''
    BIENVENIDOS AL TRABAJO PRACTICO DEL GRANDIOSO GRUPO 2!
    Integrantes:
    Tomas "El Mago" Corsico
    Enzo "El Magnifico" Herbas
    '''
    + Back.RESET + Back.LIGHTBLUE_EX + Fore.WHITE +
    "Trabajo practico: CRUX, EL ROBOT QUE QUERIA APRENDER A AMAR"
    + Back.RESET + Fore.WHITE +
    '''
    CRUX es un bot que hara uso remoto de una pagina de Facebook, mediante
    dialogos ingresados por el usuario, se podran realizar distintos tipos de
    acciones como las siguientes a mencionar:
    '''
    + Fore.BLUE +
    '''
    -Ver posts del feed de la pagina, donde se veran el texto que tengan o en
     el caso de que sea una foto, se podra oberservar un aviso que es una foto
     y una URL para accer a verla
    -Dar Like y Modificar posts del feed (Se ingresara mediante la funcion de
     ver posts),se debera ingresar un numero de post, previamente indicado,
     para accionar sobre el mismo
    -Crear un post de unicamente Texto
    -Subir una foto sola o con una descripcion, los tipos de archivos
     soportados son:[Tomi pone los archivos sopotados]
    -Medir la cantidad de seguidores y likes que tiene la pagina, junto con el
     nombre de la misma
    -Actualizar datos del perfil: Telefono, email, correo electronico y foto
     de perfil. El programa detectara si son aptos, en el caso contrario se
     deberan volver a ingresar.
    -Finalizar programa, mediante una despedida.
    '''
    + Fore.WHITE +
    '''
    Como tiene grandes capacidades, tambien hay que tener cuidado en ciertos
    aspectos:
    '''
    + Fore.RED +
    '''
    *Al ser un bebe bot, no esta del todo acostumbrado a largas frases
     otorgadas por el usuario por ello mismo, suele confundirse al ingresar
     largas cadenas de texto o peticiones
    *No se pudieron conseguir ciertos puntos solicitados, por el tema de los
     permisos que otorga Facebook actualmente, entre ellas estan : BUSCAR
     USUARIOS, LISTAR AMIGOS Y SEGUIDORES, SEGUIR USUARIO O SOLICITAR AMISTAD,
     ENVIAR MENSAJE A UN USUARIO
    *Se intento cubrir todo tipo de errores posibles, como el uso del TOKEN DE
     ACCESO, el cual dura unicamente 2 meses como mucho. Para encontrar otro
     token de acceso, comunicarse con el soporte
    '''
    + Fore.WHITE +
    '''
    Para el correcto uso de CRUX, se recomienda seguir los siguientes consejos:
    '''
    + Fore.GREEN +
    '''
    #Como se menciono previamente, CRUX no se lleva bien con largas frases o
     dialogos complejos, por eso mismo se recomienda una diccion en lo posible
     lo mas sencilla y directa posible para su correcto funcionamiento!
    #Aca les dejamos una lista de archivos soportados para la subida de
     imagenes: [TOMI ACA PA]
    #Nuestro Lil CRUX a veces se atolondra y no da buenas respuestas y al ser
     el programa manejado por el, suele tirar para cualquier lado, les pedimos
     paciencia y que reinicie el programa. Crux es un bebe, todos fuimos bebes
     o lo seguimos siendo en algunos casos.
    #Si aun asi los errores perstisten, se recomienda encarecidamente borra el
     archivo que se generar en la carpeta del programa el cual se llama
     "db.sqlite3", el cual es como un registro de memoria de CRUX, con ello se
     reiniciara y podra dar un mejor funcionamiento.
    '''
    + Fore.WHITE +
    '''
    Sin mas preambulos, los dejamos con el programa. Esperamos que lo disfruten!
    Saludos de parte de Enzo y Tomas!
    ''')

    '''
    PRE:
    Se entrenara al bot mediante las librerias de CHATTERBOT, se abre el
    archivo de entrenamiento "trainer.txt" y procede a entrenar al bot
    mediante cada linea, que pasaran a ser listas
    POST:
    Las respuestas seras guardadas dentro de una lista llamada "respuestas"
    con el fin de usarlas de frases clave para navegar dentro de las opciones
    del menu
    '''
    print("Bienvenido al Bot de CRUX!!")


def main():
    informacion_inicial()
    nombre_usuario, datos_api, datos_api_sdk, crux_bot, log, conexion = datos()
    if conexion is True:
        entrenamiento = entrenamiento_bot(crux_bot)
        charla = conversacion(nombre_usuario, datos_api, datos_api_sdk, crux_bot, entrenamiento, log)
    else:
        print("No hay conexion a internet. Establezca una conexion y vuelva a ejecutar el programa.")
    log.close()


main()
