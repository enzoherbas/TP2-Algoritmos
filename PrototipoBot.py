from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
CRUX = ChatBot("Cosa")
def entrenamiento_crux():
    entrenamiento = ListTrainer(CRUX)
    texto = open("trainer.txt")
    respuestas = []
    for linea in texto:
        linea = linea.rstrip("\n").split(",")
        entrenamiento.trainer(linea)
        respuestas.append(linea[-1])
    respuestas.pop(0)
    texto.close()
    return respuestas
def opciones_bot():
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
def like_posteo():
    print("Likear posteo")
    return True
def ver_posteos():
    print("Leer posteo")
    return True
def subir_post():
    print("Subir post")
    return True
def actualizar_post():
    print("Actualizar post")
    return True
def cantidad_seguidores():
    print("Lista amigos")
    return True
def actualizar_datos():
    print("Actualizar datos")
    return True
def finalizar():
    return False
def conversacion(usuario,respuestas):
    continuar = True
    while continuar == True:
        peticion = input("{0}:".format(usuario))
        respuesta = CRUX.get_response(peticion)
        if respuesta in respuestas:
            indice_respuesta = respuestas.index(respuesta)
            continuar = selector_opciones(indice_respuesta) 
def selector_opciones(respuesta):
    opciones = {
                "Vamos a ver las opciones!":opciones_bot(),
                "Entonces vamos a ver en que posteo deseas dar tu like":like_posteo(),
                3:ver_posteos(),
                4:subir_post(),
                5:actualizar_post(),
                6:cantidad_seguidores(),
                7:actualizar_datos(),
                8:finalizar()
                }
    return respuesta
def main():
    entrenamiento = entrenamiento_crux()
    usuario = input("Ingrese su nombre: ")
    charla = conversacion(usuario,entrenamiento)
main()