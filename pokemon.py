
import json
import requests


class Pokemon:
    def __init__(self, pokemon_id_or_name):
        self.pokemon_id_or_name = pokemon_id_or_name
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id_or_name}/"
        pokemon_data = requests.get(url).json()
        self.pokemon_name = pokemon_data['name']
        self.pokemon_id = pokemon_data['id']
        self.pokemon_types = pokemon_data['types']
        self.pokemon_sprite = pokemon_data['sprites']['front_default']
        generation_url = pokemon_data['species']['url']
        generation_data = requests.get(generation_url).json()
        generation_num = generation_data['generation']['url'].split("/")[-2]
        self.pokemon_generation = int(generation_num)



