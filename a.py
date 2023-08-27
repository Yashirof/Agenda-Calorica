import requests

def req(comida):
    url = f'https://caloriasporalimentoapi.herokuapp.com/api/calorias/?descricao={comida}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data:
            return data[0]  # Retorne apenas a primeira entrada encontrada

    return None
