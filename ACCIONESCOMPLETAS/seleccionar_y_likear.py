import json
from pyfacebook import Api
datos_app = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )

def data_posts_pagina(pagina_id):  
    data = datos_app.get_page_posts(page_id=pagina_id,return_json=True,)
    return data

def filtrar_id_posts():
    pagina_id= "341526406956810"
    data_posts = data_posts_pagina(pagina_id)
    posts_id = []
    contador_posts = 1
    for variable_data in data_posts :
        print("N°{0} Post.\n-{1}"
              .format(contador_posts,variable_data["message"]))
        post_id = (contador_posts,variable_data["id"])
        posts_id.append(post_id)
        contador_posts += 1
    return dict(posts_id)

def publicar_like(datos_app,id_post):
    post_args = { "access_token":datos_app._access_token}
    peticion = datos_app._request(path="v9.0/{0}/likes".format(id_post),method="POST",post_args = post_args)
    data = datos_app._parse_response(peticion)
    print("Se ha puesto un like, exitosamente!")
    
def seleccionar_post_like(datos_app,posts_id):
    seleccion_numero_post = int(input("Selecciona que numero de post deseas dar like."))
    id_post = posts_id[seleccion_numero_post]
    like = publicar_like(datos_app,id_post)
                 
def main():
    posts_id = filtrar_id_posts()
    seleccionar_post_like(datos_app,posts_id)    

main()