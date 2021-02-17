import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyfacebook import Api

DATOS = Api(app_id = "692001264799472",app_secret = "60b272a45b500fef45f3c930d5d6d8df",long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",)
ID_PAGINA = "341526406956810"
CRUX = ChatBot("prototipo_bot",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Disculpa, no logro entenderte. Intenta escribirlo de otra manera',
            'maximum_similarity_threshold': 0.80
        }
    ])

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
    texto = open("trainer.txt")
    respuestas = []
    contador = 0
    for linea in texto:
        linea = linea.rstrip("\n").split(",")
        #entrenamiento.train(linea)
        if linea[-1] not in respuestas and contador <= 8:
            respuestas.append(linea[-1])
            contador += 1
    print(respuestas)
    texto.close()
    return respuestas

def opciones_bot():
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
    print("Se logro likear con exito el post!")
    return True

def ver_posteos():
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
                contador_posts += 1 
            except:
                print("N°{0} Post.\n-Imagen\n-Url: {1}".format(contador_posts,informacion_post["permalink_url"]))
                contador_posts += 1 
            post_id = (contador_posts,informacion_post["id"])
            posts_id.append(post_id)
    dicc_posts = dict(posts_id)
    finalizar_modificaciones = False
    while finalizar_modificaciones == False:        
        eleccion_modificacion = input("Deseas realizar una modificacion?\nIngrese SI o NO")
        if eleccion_modificacion == "SI":
                numero_post_elegido = int(input("Ingrese el numero de post a modificar: "))
                selector_modificacion = input("Ingrese ME GUSTA o CAMBIAR TEXTO para realizar la accion: ")
                if selector_modificacion == "ME GUSTA":
                    like_posteo(dicc_posts[numero_post_elegido])   
                else:
                    actualizar_post(dicc_posts[numero_post_elegido])                
        else:
            finalizar_modificaciones = True
            
    return True

def subir_posteo():
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
    print("El posteo se actualizo con exito!")

def cantidad_seguidores():
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

def actualizar_datos():
    '''
    Actualiza los datos de la pagina
    '''
    cambios = {
        1:("Descripcion de pagina","about"),
        2:("Email","emails"),   
        3:("Telefono","phone")
        }
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
            cambio = input(f"Ingrese su nuevo/a {cambios[opcion][0]}: ".capitalize())
            if opcion == 2:
                cambio = cambio.split()
            post_args = {"Access token":DATOS._access_token}
            peticion = DATOS._request(path = f"v9.0/{ID_PAGINA}?{cambios[opcion][1]}={cambio}", method = "POST", post_args = post_args)
            data = DATOS._parse_response(peticion)
            continuar = True 
        except:
            if opcion == 2:
                print("Debe ingresar un email valido.")
            else:
                print("Debe ingresar un numero de telefono valido.")
    print("Se modificaron los datos con exito!")
    return True

def subir_foto():
    '''
    Hay que ver si se junta junto con la funcion SUBIR_POSTEO
    '''
    print("Subir Foto")
    return True

def finalizar():
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
    Se generara una charla con el nombre del usuario y del bot. Desde aca se redigiran a las distintas opciones
    POST:
    Se guardara una charla en el LOG (Aun no creado) donde estara NOMBRE, HORA Y TEXTO EMITIDO
    '''
    continuar = True
    while continuar == True:
        peticion = input("{0}:".format(usuario))
        respuesta_bot = CRUX.get_response(peticion)
        print("Crux:{0}".format(respuesta_bot))
        if str(respuesta_bot) in respuestas_clave:
            indice_respuesta = respuestas_clave.index(str(respuesta_bot)) 
            continuar = selector_opciones(indice_respuesta)
            
def selector_opciones(respuesta):
    '''
    Diccionario de funciones a ingresar mediante a la respuesta que dara el BOT
    '''
    opciones = {0:opciones_bot,
                1:ver_posteos,
                2:like_posteo,
                3:actualizar_post,                
                4:subir_posteo,
                5:subir_foto,
                6:cantidad_seguidores,
                7:actualizar_datos,
                8:finalizar
                }
    accion = opciones[respuesta]()
    return accion

def main():
    entrenamiento = entrenamiento_bot()
    usuario = input("Ingrese su nombre: ")
    charla = conversacion(usuario,entrenamiento)
    print("FIN")
    
main()