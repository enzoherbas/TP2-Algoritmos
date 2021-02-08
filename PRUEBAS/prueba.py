texto = open("prueba.txt")
contador = 0
respuestas = []
for linea in texto:
    linea = linea.rstrip("\n").split(",")
    respuestas.append(linea[-1])
respuestas.pop(0)
print(respuestas)
def opciones_bot():
    print('''
    -Buscar usuarios
    -Reaccionar posteos

          
          ''')
def