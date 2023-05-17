# This is the best project ever.
import random
from flask import Flask, request, Response
import requests
from pokemon import Pokemon

app = Flask(__name__)


def get_random_pokemon():
    """Returns a random pokemon from the full list of pokemon"""
    pokemon = Pokemon(random.randint(0, 1008))
    return pokemon


@app.route('/')
def home():
    html = '''
            <html>
                <body>
                <ul style="list-style:none">
                <title>Trev and Afek Pokemon Project</title>
                    <h1>Trev and Afek Pokemon Project</h1>
                    <li><a href="/whos-that-pokemon">Who's That Pokemon?</a></li>
                    <li><a href="/type-quiz">Type Quiz</a></li>
                    <li><a href="/pokemon-search">Pokemon Search</a></li>
                </ul>
            </body>
            </html>
        '''
    return html


@app.route('/whos-that-pokemon', methods=['GET', 'POST'])
def whos_that_pokemon():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon-name'].lower()
        correct_answer = request.form['correct_answer'].lower()
        if pokemon_name == correct_answer:
            pokemon = Pokemon(correct_answer)
            return f'''
                <html>
                    <head>
                        <title>Confirmation Page</title>
                    </head>
                    <body>
                        <h1>Congratulations, you got it right!</h1>
                        <img src="{pokemon.pokemon_sprite}" alt="{correct_answer} image">
                        <h1><a href="/">Go back to home</a></h1>
                    </body>
                </html>
            '''
        else:
            correct_pokemon = Pokemon(correct_answer)
            pokemon_name = correct_pokemon.pokemon_name
            types_str = ""
            for t in correct_pokemon.pokemon_types:
                types_str += t['type']['name'] + ", "
            pokemon_type = types_str[:-2]
            pokemon_id = correct_pokemon.pokemon_id
            pokemon_generation = correct_pokemon.pokemon_generation
            message = f'Incorrect! Please try again. The typing is {pokemon_type} and it was introduced in generation {pokemon_generation}'
            message2 = f'Description: {correct_pokemon.pokemon_desc}'
    else:
        pokemon = get_random_pokemon()
        pokemon_name = pokemon.pokemon_name
        types_str = ""
        for t in pokemon.pokemon_types:
            types_str += t['type']['name'] + ", "
        pokemon_type = types_str[:-2]
        pokemon_id = pokemon.pokemon_id
        pokemon_generation = pokemon.pokemon_generation
        message = f'Guess the Pokemon with typing {pokemon_type}, introduced in generation {pokemon_generation}.'
        message2 = f'Description: {pokemon.pokemon_desc}'

    html = f'''
        <html>
            <head>
                <title>Who's That Pokemon?</title>
            </head>
            <body>
                <h1>Who's That Pokemon?</h1>
                <p>{message}</p>
                <p>{message2}</p>
                <form method="post">
                    <input type="text" name="pokemon-name">
                    <input type="hidden" name="correct_answer" value="{pokemon_name}">
                    <input type="submit" value="Guess">
                </form>
            </body>
        </html>
    '''
    return html


@app.route('/type-quiz', methods=['GET', 'POST'])
def type_quiz():
    if request.method == 'POST':
        pokemon = Pokemon(request.form['pokemon-name'])
        user_types = request.form['pokemon-types'].lower().replace(" ", "").split(',')
        correct_types = sorted([t['type']['name'] for t in pokemon.pokemon_types])

        if sorted(user_types) == sorted(correct_types):
            return '''
                <html>
                    <head>
                        <title>Confirmation Page</title>
                    </head>
                    <body>
                        <h1>Congratulations, you got it right! Trevor and Afek love you!</h1>
                        <h1><a href="/">Go back to home</a></h1>
                    </body>
                </html>
            '''
        else:
            message = "Incorrect! Please try again. Use a comma to separate the types!"

    else:
        pokemon = get_random_pokemon()
        message = f"What are the types of {pokemon.pokemon_name}? Format like this: 'type1,type2'. Don't use spaces!"

    types_str, pokemon_type = get_type_strings(pokemon)

    html = f'''
        <html>
            <head>
                <title>Type Quiz</title>
            </head>
            <body>
                <h1>Type Quiz</h1>
                <p>{message}</p>
                <img src="{pokemon.pokemon_sprite}" alt="{pokemon.pokemon_name} sprite">
                <form method="post">
                    <input type="text" name="pokemon-name" value="{pokemon.pokemon_name}" style="display:none">
                    <input type="text" name="correct_types" value="{pokemon_type}" style="display:none">
                    <input type="text" name="pokemon-types">
                    <input type="submit" value="Guess">
                </form>
            </body>
        </html>'''
    return html


@app.route('/pokemon-search', methods=['GET', 'POST'])
def pokemon_search():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon-name'].lower()
        pokemon = Pokemon(pokemon_name)
        types_str = ""
        for t in pokemon.pokemon_types:
            types_str += t['type']['name'] + ", "
        pokemon_type = types_str[:-2]

        return f'''
            <html>
                <head>
                    <title>Pokemon Details</title>
                </head>
                <body>
                    <h1>{pokemon.pokemon_name}</h1>
                    <p>ID: {pokemon.pokemon_id}</p>
                    <p>Type: {pokemon_type}</p>
                    <img src="{pokemon.pokemon_sprite}" alt="{pokemon_name} image">
                    <h1><a href="/">Go back to home</a></h1>
                </body>
            </html>
        '''
    else:
        return '''
            <html>
                <head>
                    <title>Pokemon Details</title>
                </head>
                <body>
                    <h1>Enter a Pokemon's Name or ID</h1>
                    <form method="post">
                        <input type="text" name="pokemon-name">
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
        '''


def get_type_strings(pokemon):
    types_str = ""
    for t in pokemon.pokemon_types:
        types_str += t['type']['name'] + ", "
    pokemon_type = types_str[:-2]
    return types_str, pokemon_type


if __name__ == '__main__':
    app.run(debug=True)
