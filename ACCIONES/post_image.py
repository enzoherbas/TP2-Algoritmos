import facebook
from tkinter import Tk
from tkinter.filedialog import askopenfilename

long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",

api = facebook.GraphAPI(long_term_token)

Tk().withdraw()
filename = askopenfilename() 

def post_image():
    api.put_photo(image = open(r"{0}".format(filename),"rb"), message = input("Ingrese descripcion de la foto: "))

if __name__ == "__main__":
    post_image()