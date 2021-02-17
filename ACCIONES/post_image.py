import facebook
import facebook
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.wm_attributes('-topmost', 1)
window.withdraw()

long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",

api = facebook.GraphAPI(long_term_token)


def post_image():
        archivos_soportados = ["peg","bmp","png","gif","iff"]
        ingreso_correcto = False
        while not ingreso_correcto:
                filename = filedialog.askopenfilename()
                if filename[-3::] in archivos_soportados:
                        ingreso_correcto = True
                else:
                        print("El archivo elegido es incorrecto, vuelva a elegir.")
        api.put_photo(image = open(r"{0}".format(filename),"rb"), message = input("Ingrese descripcion de la foto: "))
        print("Se ha subido el posteo")


if __name__ == "__main__":
    post_image()
