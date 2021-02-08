from pyfacebook import Api

def get_posts(page_id):
    # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
    # pasa por parámetros, las constantes anteriormente definidas.
    api = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABALbobzkx1tBsgqpYdsjSns3uDQPNaHOZANCBMGiuDxnymMPVqGG1RwvD3K5vnf0Mnc49YPNx6ZCuKSGAWub0EVn67TIHQHvyZChMJq1ypRN3z8BjkeXkqFqf3g2B5M7yfi4S2Qw9lJpWkmfyjtURjpGuhdhgpbEZBPEeNW8GBSV3oDgKeyMnRTQ14ZBfe6WMMHWgZCOnui3tfcE5pytIcVxNZAbyHjqAlPejznf53ZCgPlqO4q6ssOYZD",
    )

    # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
    # el usuario, en su muro.
    # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
    # información se desea obtener.
    data = api.get_page_posts(
        page_id = page_id,
        since_time = "2020-05-01",
        count = None,
        limit = 100,
        return_json = False,
    )

    return data


def processor():
    # En este campo, se debe setear el id de usuario. El mismo se obtiene desde la cuenta
    # normal de Facebook en "Configuración/Integraciones comerciales", y en la aplicación
    # que se creó, dar click en "Ver y editar".
    # También se puede obtener desde Facebook for Developers, haciendo una consulta desde
    # el "Explorador de la API Graph"
    page_id = "341526406956810"
    data = get_posts(page_id)

    return data


if __name__ == "__main__":
    processor()