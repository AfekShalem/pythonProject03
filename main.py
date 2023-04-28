# This is the best project ever.
import json
import requests


def get_pokemon_data(pokemon_id_or_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id_or_name}/"
    data = requests.get(url)
    return data


class Quiz:

    def __init__(self, quiz_type, gen):
        self.quiz_type = quiz_type
        self.gen = gen

