# This is the best project ever.
import random
from flask import Flask, request, Response
import requests


def get_pokemon_data(pokemon_id_or_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id_or_name}/"
    data = requests.get(url)
    return data.json()


app = Flask(__name__)


@app.route('/')
def home():
    html = '''
            <html>
                <body>
                <ul style="list-style:none">
                    <li><a href="/whos-that-pokemon">Who's That Pokemon?</a></li>
                    <li><a href="/type-quiz">Type Quiz</a></li>
                </ul>
            </body>
            </html>
        '''
    return html


@app.route('/whos-that-pokemon', methods=['GET', 'POST'])
def whos_that_pokemon():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon-name'].lower()
        correct_answer = request.form['correct_answer']
        if pokemon_name == correct_answer:
            pokemon_data = get_pokemon_data(correct_answer)
            pokemon_name = pokemon_data['name']
            pokemon_image_url = pokemon_data['sprites']['front_default']
            return f'''
                <html>
                    <head>
                        <title>Confirmation Page</title>
                    </head>
                    <body>
                        <h1>Congratulations, you got it right!</h1>
                        <img src="{pokemon_image_url}" alt="{pokemon_name} image">
                    </body>
                </html>
            '''
        else:
            message = 'Incorrect! Please try again.'
            pokemon_data = get_pokemon_data(correct_answer)
            pokemon_name = pokemon_data['name']
            pokemon_type = ', '.join([t['type']['name'] for t in pokemon_data['types']])
            pokemon_id = pokemon_data['id']
            pokemon_generation = get_pokemon_generation(pokemon_id)
    else:
        pokemon_data = get_random_pokemon()
        pokemon_name = pokemon_data['name']
        pokemon_type = ', '.join([t['type']['name'] for t in pokemon_data['types']])
        pokemon_id = pokemon_data['id']
        pokemon_generation = get_pokemon_generation(pokemon_id)
        message = f'Guess the Pokemon with typing {pokemon_type}, introduced in generation {pokemon_generation}.'

    html = f'''
        <html>
            <head>
                <title>Who's That Pokemon?</title>
            </head>
            <body>
                <h1>Who's That Pokemon?</h1>
                <p>{message}</p>
                <form method="post">
                    <input type="text" name="pokemon-name">
                    <input type="hidden" name="correct_answer" value="{pokemon_name}">
                    <input type="submit" value="Guess">
                </form>
            </body>
        </html>
    '''
    return html


def get_random_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1118')
    pokemon_list = response.json()['results']
    pokemon_url = pokemon_list[random.randint(0, len(pokemon_list) - 1)]['url']
    pokemon_data = requests.get(pokemon_url).json()
    return pokemon_data


def get_pokemon_generation(pokemon_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/')
    generation_url = response.json()['generation']['url']
    generation_name = generation_url.split('/')[-2]
    return generation_name


class Quiz:

    def __init__(self, quiz_type, gen):
        self.quiz_type = quiz_type
        self.gen = gen


if __name__ == '__main__':
    app.run(debug=True)
