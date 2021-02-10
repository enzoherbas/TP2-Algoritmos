from pyfacebook import Api
 
datos = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )

def actualizar_post(api,post_id):
    post_args = { "access_token":api._access_token}
    peticion = api._request(path="v9.0/{0}/?message=Texto%20Cambiado%20Desde%20Api".format(post_id),method="POST",post_args = post_args)
    data = api._parse_response(peticion)
    return data

data = actualizar_post(datos,"341526406956810_350838002692317")
print(data)    
