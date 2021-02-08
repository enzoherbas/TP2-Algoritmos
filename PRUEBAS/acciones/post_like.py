from pyfacebook import Api

#def get_posts(page_id):   
datos = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAGGmtcUNCyZBZAP7Yt5rMcC1q2XcFprTPGBrGqa8mOfkXN9ic4oBOx1rYjfh1fvdcekAvsrmrl1XJ3pQ4ibIlm6lT7Rif0M2jE3Rhv8n24oWUq9yG1HHDqJrK60q2Akq4NqxPdvBX4TTAtNqdJF7uYwvBLHtVbclEaYzVsZBjLtag1R4S8DRcnGh6GjcvSoHR0DGEda",
        )

def publicar_like(api,post_id, access_token=None,  ):
    post_args = { "access_token":api._access_token}
    peticion = api._request(path="v9.0/{0}/likes".format(post_id),method="POST",post_args = post_args)
    data = api._parse_response(peticion)
    return data

data = publicar_like(datos,"341526406956810_350838002692317")
print(data)    

'''
#return data
'''