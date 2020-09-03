import aiohttp
import googlemaps
from urllib.parse import urlencode
import asyncio

api_key = open("api_key.txt", "r").read()
url_base_places = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
url_base_distance_matrix = "https://maps.googleapis.com/maps/api/distancematrix/json"


def get_coordenadas(endereco):
    '''
    função responsável por acessar o API do google maps
    informando o endereço e retornando com as corrdenadas e o place ID
    para esta função foi utilizado a biblioteca googlemaps https://github.com/googlemaps/google-maps-services-python
    '''

    gmaps = googlemaps.Client(key=api_key)
    json_data = gmaps.geocode(endereco)
    return json_data[0]['geometry']['location']['lat'], \
           json_data[0]['geometry']['location']['lng'], \
           json_data[0]['place_id']

async def get_places(latitude, longitude, tipo_lugar, session):
    '''
    função que acessa o API do google maps e a partir de coordenadas encontra o local de interesse mais proximo
    denominado pela variável 'tipo_lugar'
    '''

    parametros =  {'key': api_key,
                   'input': tipo_lugar,
                   'inputtype': 'textquery',
                   "fields": "place_id,name,permanently_closed",
                   'locationbias': f"point:{latitude},{longitude}"
                   }
    parametros_encoded_places = urlencode(parametros)
    url_places = f"{url_base_places}?{parametros_encoded_places}"
    async with session.get(url_places) as response:
        json_data_places = await response.json()

    return json_data_places['candidates'][0]['place_id']

async def get_distance(place_id_origem, place_id_destino, tipo_lugar, session):
    '''
    função que acessa o API do google maps, a partir dos places id informados
    retorna a distancia entre estes locais quando percorridos a pé
    '''

    parametros = {'key': api_key,
                  'origins': f"place_id:{place_id_origem}",
                  'destinations': f"place_id:{place_id_destino}",
                  'mode': 'walking'
                  }
    parametros_encoded_distance = urlencode(parametros)
    url_matriz_distance = f"{url_base_distance_matrix}?{parametros_encoded_distance}"
    async with session.get(url_matriz_distance) as response_distance:
        json_data_distance = await response_distance.json()
    return json_data_distance['rows'][0]['elements'][0]['distance']['text']

async def encontrar_distancia_lugar_mais_proximo(latitude, longitude, tipo_lugar, place_id_origem, session):
    '''
    função que utiliza das informações do local de origem para encontrar a distancia do local de interesse mais próximo.
    '''

    global distancias
    try:
        place_id_destino = await get_places(latitude, longitude, tipo_lugar, session)
        dist = await get_distance(place_id_origem, place_id_destino, tipo_lugar, session)

        distancias[tipo_lugar] = dist
    except:
        distancias[tipo_lugar] = '0 m'


async def main_encontrar_distancias(endereco, locais):
    '''
    função responsável por chamar a função que obtem as coordenadas e depois chamar de maneira assíncrona a função
    responsável por encontrar o local de interesse mais próximo.
    para realizar as chamadas assíncronas foi utilizado a biblioteca aiohttp https://docs.aiohttp.org/en/stable/
    '''

    global distancias
    try:
        latitude, longitude, place_id = get_coordenadas(endereco)
    except:
        distancias = {str(local): '0 m' for local in locais}
        return

    async with aiohttp.ClientSession() as session:
        tasks = [encontrar_distancia_lugar_mais_proximo(latitude, longitude, local, place_id, session) for local in locais]
        await asyncio.gather(*tasks)


def encontrar_locais_de_interesse_mais_proximos(endereco, nome_locais):
    '''
    função responsável por chamar a função pricipal de maneira assíncrona
    '''

    global distancias
    distancias = {}
    asyncio.run(main_encontrar_distancias(endereco, nome_locais))
    return distancias
