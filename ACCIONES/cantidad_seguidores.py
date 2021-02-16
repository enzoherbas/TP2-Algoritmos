from pyfacebook import Api
 
datos = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )

def crear_post(api,page_id):
    #texto_post = input("Que queres que diga el post: ")
    post_args = {"access_token":api._access_token}
    peticion = api._request(path="v9.0/{0}?fields=followers_count".format(page_id),method="GET")
    data = api._parse_response(peticion)
    print(data)
    return data

print(crear_post(datos,"341526406956810"))