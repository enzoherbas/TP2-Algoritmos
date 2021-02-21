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

DATOS = Api(app_id = "692001264799472",app_secret = "60b272a45b500fef45f3c930d5d6d8df",long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",)
API_SDK = facebook.GraphAPI("EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD")
ID_PAGINA = "341526406956810"
CRUX = ChatBot("bot_10",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Disculpa, no logro entenderte. Intenta escribirlo de otra manera',
            'maximum_similarity_threshold': 0.85
        }])

LOG = open("log.txt","a")
LOG.write("\nNueva sesion\nFecha, hora, Usuario/Crux, Mensaje\n")

def entrenamiento_bot():
    print(Back.WHITE+Fore.BLACK+
    '''
    BIENVENIDOS AL TRABAJO PRACTICO DEL GRANDIOSO GRUPO 2!
    Integrantes: 
    Tomas "El Mago" Corsico
    Enzo "El Magnifico" Herbas 
    '''
    +Back.RESET+Back.LIGHTBLUE_EX+Fore.WHITE+
    "Trabajo practico: CRUX, EL ROBOT QUE QUERIA APRENDER A AMAR"
    +Back.RESET+Fore.WHITE+
    '''
    CRUX es un bot que hara uso remoto de una pagina de Facebook, mediante dialogos ingresados 
    por el usuario, se podran realizar distintos tipos de acciones como las siguientes a mencionar:
    '''
    +Fore.BLUE+
    '''
    -Ver posts del feed de la pagina, donde se veran el texto que tengan o en el caso de que
     sea una foto, se podra oberservar un aviso que es una foto y una URL para accer a verla
    -Dar Like y Modificar posts del feed (Se ingresara mediante la funcion de ver posts),
     se debera ingresar un numero de post, previamente indicado, para accionar sobre el mismo
    -Crear un post de unicamente Texto
    -Subir una foto sola o con una descripcion, los tipos de archivos soportados son:
    [Tomi pone los archivos sopotados]
    -Medir la cantidad de seguidores y likes que tiene la pagina, junto con el nombre de la misma
    -Actualizar datos del perfil: Telefono, email, correo electronico y foto de perfil. El
     programa detectara si son aptos, en el caso contrario se deberan volver a ingresar.
    -Finalizar programa, mediante una despedida.
    '''
    +Fore.WHITE+
    '''
    Como tiene grandes capacidades, tambien hay que tener cuidado en ciertos aspectos:
    '''
    +Fore.RED+
    '''
    *Al ser un bebe bot, no esta del todo acostumbrado a largas frases otorgadas por el usuario
     por ello mismo, suele confundirse al ingresar largas cadenas de texto o peticiones
    *No se pudieron conseguir ciertos puntos solicitados, por el tema de los permisos que otorga
     Facebook actualmente, entre ellas estan : BUSCAR USUARIOS, LISTAR AMIGOS Y SEGUIDORES, SEGUIR
     USUARIO O SOLICITAR AMISTAD, ENVIAR MENSAJE A UN USUARIO
    *Se intento cubrir todo tipo de errores posibles, como el uso del TOKEN DE ACCESO, el cual dura
     unicamente 2 meses como mucho. Para encontrar otro token de acceso, comunicarse con el soporte
    '''
    +Fore.WHITE+
    '''
    Para el correcto uso de CRUX, se recomienda seguir los siguientes consejos:
    '''
    +Fore.GREEN+
    '''
    #Como se menciono previamente, CRUX no se lleva bien con largas frases o dialogos complejos,
     por eso mismo se recomienda una diccion en lo posible lo mas sencilla y directa posible para
     su correcto funcionamiento!
    #Aca les dejamos una lista de archivos soportados para la subida de imagenes: [TOMI ACA PA]
    #Nuestro Lil CRUX a veces se atolondra y no da buenas respuestas y al ser el programa manejado
     por el, suele tirar para cualquier lado, les pedimos paciencia y que reinicie el programa.
     Crux es un bebe, todos fuimos bebes o lo seguimos siendo en algunos casos.
    #Si aun asi los errores perstisten, se recomienda encarecidamente borra el archivo que se generar
     en la carpeta del programa el cual se llama "db.sqlite3", el cual es como un registro de memoria
     de CRUX, con ello se reiniciara y podra dar un mejor funcionamiento.
    '''
    +Fore.WHITE+
    '''
    Sin mas preambulos, los dejamos con el programa. Esperamos que lo disfruten!
    Saludos de parte de Enzo y Tomi!
    ''')
    
    '''
    PRE:
    Se entrenara al bot mediante las librerias de CHATTERBOT, se abre el archivo de
    entrenamiento "trainer.txt" y procede a entrenar al bot mediante cada linea,
    que pasaran a ser listas
    POST:
    Las respuestas seras guardadas dentro de una lista llamada "respuestas" con el
    fin de usarlas de frases clave para navegar dentro de las opciones del menu
    '''
    entrenamiento = ListTrainer(CRUX, show_training_progress = False)
    texto_entrenamiento = open("trainer.txt")
    respuestas_clave = []
    for linea_de_dialogo in texto_entrenamiento:
        linea_de_dialogo = linea_de_dialogo.rstrip("\n").split(",")
        entrenamiento.train(linea_de_dialogo)
        if len(respuestas_clave) <= 9:
            respuestas_clave.append(linea_de_dialogo[-1])
    texto_entrenamiento.close()
    return respuestas_clave

def opciones_bot(usuario):
    '''
    PRE:
    Se ingresara una vez sea solicitado este menu, es un printeo de las opciones las cuales se
    pueden realizar, para que el usuario pueda realizar las tareas que desee.
    POST:
    Se retira de la funcion sin ningun cambio y se reingresara en el caso que se vuelva a llamar
    las veces que sean falta.
    '''
    print('''
    -Ver posteos
    -Subir foto
    -Subir posteo
    -Actualizar post
    -Cantidad de seguidores
    -Actualizar datos del perfil
    -Salir          
    ''')
    return True

def like_posteo(post_id):
    '''
    PRE:
    Se ingresa mediante la funcion de "modificacion_post" para con el ID enviado, se puede elegir el
    post a modificar. Con el ID recibido se genera la peticion que va realizar el posteo del Like
    al posteo deseado.
    POST:
    No devuelve nada, desde aca se genera toda la peticion necesaria.
    '''
    post_args = {"access_token":DATOS._access_token}
    peticion = DATOS._request(
        path="v9.0/{0}/likes".format(post_id),
        method="POST",
        post_args = post_args)

def ver_posteos(usuario, respuestas):
    '''
    PRE:
    Se ingresa mediante el menu de dialogo del BOT, desde aca se veran los posts y realizaran las
    modificaciones a los mismos.Se analiza el feed, cada publicacion individual y se evalua cuales
    son aptos para las modificaciones. Ya que solo los posteos,que no son modificaciones de perfil,
    son aptos para modificaciones.
    POST:
    Se envia los datos recolectados como el ID de cada publicacion, con el fin de poder realizar la
    modificacion. En este caso las modicaciones se enviaran a "modificacion_posts" para seguir con las
    ordenes de modificacion
    '''
    posts_id = []
    informacion_posts = DATOS.get_page_posts(
        page_id = ID_PAGINA,
        fields= "story,message,permalink_url,created_time",
        return_json = True,
        count=None)
    cantidad_post = 1
    for informacion_post in informacion_posts:
        fecha_post = informacion_post["created_time"].split("T")
        if ("story") not in informacion_post:
            try:
                print('''
                         PUBLICACION N°{0}                 {1}
                         ////////////////////////////////////////////
                         Texto del Post:{2}'''
                         .format(cantidad_post,fecha_post[0],informacion_post["message"]))
                post_id = (cantidad_post,informacion_post["id"])
                posts_id.append(post_id)
                cantidad_post += 1
            except:
                print('''
                         PUBLICACION N°{0}                  {1}
                         ////////////////////////////////////////////
                         El POST es una imagen!
                         
                         -URL de imagen: {2}'''
                         .format(cantidad_post,fecha_post[0],informacion_post["permalink_url"]))
                post_id = (cantidad_post,informacion_post["id"])
                posts_id.append(post_id)
                cantidad_post += 1
    dicc_posts = dict(posts_id)
    modificacion_posts(dicc_posts,usuario,cantidad_post,respuestas)
    return True

def subir_posteo(usuario):
    '''
    PRE:
    Se ingresa mediante la conversacion con el bot, desde aca podremos realizar
    una creacion de post. Que sea unicamente de texto.
    POST:
    Se sube el posteo al feed de la PAGINA, y no se realizan mas cambios que ello.
    Se vuelve a la charla con el BOT.
    '''
    acciones_bot("seccion7")
    texto_post= acciones_usuario(usuario)
    post_args = {"message":texto_post,"access_token":DATOS._access_token}
    peticion = DATOS._request(
        path="v9.0/{0}/feed".format(ID_PAGINA),
        method="POST",
        post_args = post_args)
    acciones_bot("seccion8")
    return True

def actualizar_post(post_id):
    '''
    PRE:
    Se adquiere el ID del post a actualizar mediante la funcion "modifacion_posts". Se le ingresara un
    nuevo texto al posteo elegido
    '''
    modificacion_mensaje = input("Ingrese el nuevo texto del post: ")
    post_args = {"access_token":DATOS._access_token,"message":modificacion_mensaje}
    peticion = DATOS._request(
        path="v9.0/{0}".format(post_id,modificacion_mensaje),
        method="POST",
        post_args = post_args)

def eliminar_post(post_id):
    '''
    PRE: Se abre desde la funcion "modificacion_posts", para poder eliminar el post seleccionado.
    '''
    args = {"method":"delete","access_token":DATOS._access_token}
    peticion = DATOS._request(
        path="v9.0/{0}".format(post_id),
        post_args=args,
        method="POST")
    data = DATOS._parse_response(peticion)

def modificacion_posts(id_posts,usuario,cantidad_post,respuestas):
    '''
    PRE: Se ingresan los id_posts para poder realizar la modificacion deseada mediante la charla
    con el bot y una parte con el sistema para evitar errores con la palabra de afirmacion. la
    cantidad de posts tambien para corroborar que la eleccion de post a modificar este dentro de
    los rangos de eleccion, las "respuestas" ingresan con el fin de corroborar que la respuesta
    del bot sea la deseada e ingrese a las funciones "like_post", "actualizar_post" o "eliminar_post"
    POST: Retora a la opcion anterior de "VER_POSTEOS" para verificar si desea seguir con las
    modificaciones.
    '''
    acciones_bot("seccion1")
    respuesta_usuario = input("{0}:".format(usuario)).upper()
    registro_log(respuesta_usuario,usuario)
    if respuesta_usuario == "SI":
        eleccion_modificacion = True
        while eleccion_modificacion == True:
            acciones_bot("seccion2")
            numero_post_elegido = acciones_usuario(usuario)
            try:
                if numero_post_elegido.isnumeric and int(numero_post_elegido) < cantidad_post:
                    eleccion_modificacion = False
                else:
                    acciones_bot("seccion4")
            except:
                acciones_bot("seccion4")
        finalizar_accion = False
        while finalizar_accion == False:
            acciones_bot("seccion5")
            selector_modificacion = mensajes(usuario)
            if str(selector_modificacion) == respuestas[7]:
                like_posteo(id_posts[int(numero_post_elegido)])
                acciones_bot("seccion6")
                finalizar_accion = True
            elif str(selector_modificacion) == respuestas[8]:
                actualizar_post(id_posts[int(numero_post_elegido)])
                acciones_bot("seccion6")
                finalizar_accion = True
            elif str(selector_modificacion) == respuestas[9]:
                eliminar_post(id_posts[int(numero_post_elegido)])
                acciones_bot("seccion6")
            else:
                acciones_bot("seccion4")
    else:
        acciones_bot("seccion3")
        eleccion_modificacion = True
        
    print(eleccion_modificacion)
    return eleccion_modificacion

def cantidad_seguidores(usuario):
    '''
    PRE:
    Muestra la cantidad de seguidores,likes y nombre que tiene la pagina
    '''
    argumentos_get = {"fields" : "followers_count,fan_count,name"}
    peticion = DATOS._request(
        path="v9.0/{0}?".format(ID_PAGINA),
        args=argumentos_get,
        method="GET")
    data = DATOS._parse_response(peticion)
    estadisticas_pagina = ('''
          La cantidad de personas que interactuan con la pagina "{2}"
          son 
          {0} Followers 
          {1} Likes en la pagina
          '''.format(data["followers_count"],data["fan_count"],data["name"]))
    print("Crux: {}".format(estadisticas_pagina))
    registro_log(estadisticas_pagina,"Crux")
    return True

def foto_archivo(page_id, usuario, accion):
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()
    archivos_soportados = ["peg","bmp","png","gif","fif"]
    try:
        ingreso_correcto = False
        while not ingreso_correcto:
            filename = filedialog.askopenfilename()
            if filename[-3::] in archivos_soportados:
                if accion == True:
                    API_SDK.put_photo(image = open(r"{0}".format(filename),"rb"), album_path=f"{page_id}/picture")
                    ingreso_correcto = True
                elif accion == False:
                    acciones_bot("cod22")
                    API_SDK.put_photo(image = open(r"{0}".format(filename),"rb"), message = acciones_usuario(usuario))
                    ingreso_correcto = True
                    acciones_bot("cod14")
            else:
                acciones_bot("cod13")
                salir = acciones_usuario(usuario)
                if salir == "si":
                    ingreso_correcto = False
                else:
                    ingreso_correcto = True
    except:
        acciones_bot("cod14")

def foto_url(page_id, usuario, accion):
    ingreso_correcto = False
    while not ingreso_correcto:
        try:
            acciones_bot("cod23")
            url = acciones_usuario(usuario)
            if accion == True:
                post_args = {"picture":url,"access_token":DATOS._access_token}
                peticion = DATOS._request(
                    path=f"v9.0/{page_id}/picture",
                    method="POST",
                    post_args = post_args)
                data = DATOS._parse_response(peticion)
                print(data)
                ingreso_correcto = True
            if accion == False:
                acciones_bot("cod22")
                mensaje = acciones_usuario(usuario)
                post_args = {"url":url,"access_token":DATOS._access_token,"caption":mensaje}
                peticion = DATOS._request(
                    path=f"v9.0/{page_id}/photos",
                    method="POST",
                    post_args = post_args)
                data = DATOS._parse_response(peticion)
                ingreso_correcto = True
        except pyfacebook.error.PyFacebookException as error:
            if "(#100) picture should represent a valid URL" or "(#100) url should represent a valid URL "== error.message:
                acciones_bot("cod16")
            elif "Missing or invalid image file" or "Invalid parameter" == error.message:
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
    peticion = DATOS._request(
        path = f"v9.0/{page_id}/picture",
        method = "POST",
        post_args = post_args)
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
            foto_archivo(page_id, usuario, True)
        if opcion_2 == 2:
            foto_url(page_id, usuario, False)
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
            continuar = False
        else:
            finalizar = True
            acciones_bot("cod20")
    return True

def subir_foto(usuario):
    '''
    Hay que ver si se junta junto con la funcion SUBIR_POSTEO
    '''
    acciones_bot("cod21")
    print("1. Seleccionando archivo\n2. Mediante URL")
    opcion = validacion_en_rango(1, 3, usuario)
    if opcion == 1:
        foto_archivo(ID_PAGINA, usuario, False)
    if opcion == 2:
        foto_url(ID_PAGINA, usuario, False)
    acciones_bot("cod14")
    acciones_bot("cod20")
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
    Toma el nombre del usuario y las respuestas previamente guardadas del entrenamiento
    de crux en ENTRENAMIENTO_BOT. Se generara una charla con el nombre del usuario y del bot.
    POST:
    Se redirecciona a las distintas funciones y a medida que ocurre se generan los cambios
    en el LOG. La charla continua hasta que el usuario decida Finalizarla mediante la
    conversacion con el bot
    '''
    opciones = {0:opciones_bot,
                1:ver_posteos,
                2:subir_posteo,
                3:subir_foto,
                4:cantidad_seguidores,
                5:actualizar_datos,
                6:finalizar
                }
    acciones_bot("saludo inicial")
    
    continuar = True
    while continuar == True:
        respuesta_bot = mensajes(usuario)
        if str(respuesta_bot) in respuestas_clave:
            indice_respuesta = respuestas_clave.index(str(respuesta_bot))
            if indice_respuesta in range (2,7) or indice_respuesta is 0:
                continuar = opciones[indice_respuesta](usuario)
            elif indice_respuesta is 1:
                continuar = opciones[indice_respuesta](usuario,respuestas_clave)
            
def registro_log (dialogo,usuario):
    '''
    PRE:
    Ingresa el dialogo junto al usuario para poder ingresarlo al log en forma de dialogo
    con el dia y hora del momento del mensaje.
    POST:
    Devuelve el archivo LOG con las nuevas modificaciones.
    '''
    hora_actual = datetime.now()
    dialogo_log = str("{0} {1}:{2}:{3} {4} : {5}".format(
        date.today(),#0
        hora_actual.hour,#1
        hora_actual.minute,#2
        hora_actual.second,#3
        usuario,#4
        dialogo))#5
    LOG.write(dialogo_log+"\n")

def mensajes(usuario):
    '''
    PRE:
    Se ingresan los datos del usuario para poder registrarlo en el LOG, se genera una conversacion
    de respuesta con el bot 
    POST:
    El bot devuelve una respuesta, que abrira o no una funcion con respecto en donde se use. Se
    comparara esa respuesta en la lista de palabras claves para ver si esta en ellas esa respuesta
    otorgada.
    '''
    peticion = input("{0}:".format(usuario))
    registro_log(peticion,usuario)
    peticion = peticion.lower()
    respuesta_bot = CRUX.get_response(peticion)
    registro_log(respuesta_bot,"Crux")
    print("Crux:{0}".format(respuesta_bot))
    return respuesta_bot

def acciones_bot(codigo_accion):
    '''
    PRE:
    Se ingresa un "codigo_accion" que no es mas que una cadena de texto que esta diseñada para
    poder abrir una funcion en especifico, se utilizara a lo largo del programa
    POST:
    Printea la respuesta del bot con respecto a ese "codigo_accion" y se guardara en el LOG
    '''
    lectura_accion = CRUX.get_response(codigo_accion)
    print("Crux: {0}".format(lectura_accion))
    registro_log(lectura_accion,"Crux")

def acciones_usuario(usuario):
    '''
    PRE:
    Se ingresa el usuario para generar un dialogo del USUARIO en distintas instancias del
    funcionamiento del programa.
    POST:
    Retorna esa accion del usuario que sera leida por el bot y generara una respuesta
    tambien el dialogo se guardara en el LOG
    '''
    accion_usuario = input("{0}: ".format(usuario))
    registro_log(accion_usuario,usuario)
    return accion_usuario.lower()

def main():
    entrenamiento = entrenamiento_bot()
    print("Bienvenido al Bot de CRUX!!")
    usuario = input("Por favor, ingrese su usuario: ")
    charla = conversacion(usuario,entrenamiento)
    LOG.close()
    print("FIN")

main()