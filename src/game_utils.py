"""
Utilities for the game including random selections and prompts.
"""
import random
import string

ALPHABET = string.ascii_lowercase + string.digits
ID_LENGTH = 8


def game_id():
    return ''.join(random.choices(ALPHABET, k=ID_LENGTH)) # Using this instead of uuid for shorter game ids


def random_animal():
    return random.choice(available_animals)


available_animals = ["Giraffe", "Elephant", "Lion", "Zebra", "Monkey", "Gorilla"]


def random_names(number_of_samples : int) -> list[str]:
    return random.sample(available_names, number_of_samples)


available_names = ["Jack", "Jill", "Bob", "Courtney", "Fizz", "Mallory"]


def random_index(number_of_players : int) -> int:
    return random.randint(0, number_of_players - 1)


def fetch_prompt(prompt_name):
    return prompts[prompt_name]


_game_rules = '''\
GAME RULES: You are playing a social deduction game where every player pretends the be the same animal. 
During the round players go around the room and make an "I"-statement as if they were the animal. 
All players know what animal they are pretending to be, except one who is known as the Chameleon. The Chameleon and must blend in by providing details about the animal using context from other players. 
The other players must be careful not to give away too much information with their responses so that Chameleon cannot guess the animal. After all players have spoken, they vote on who they think the Chameleon is. 

'''

_herd_animal = """\
You are a {animal}, keep this a secret at all costs. 
In 10 words or less give a description of yourself starting with "I". The description should not give away too much information about the {animal} as you do not want the Chameleon to be able to guess what animal you are. Do not repeat responses from other players.
If the Chameleon can guess what animal you really are you will LOSE.
Previously Mentioned Descriptions: 
{player_responses}
"""

_chameleon_animal = """\
You are the Chameleon, keep this a secret at all costs. 
You don't know what animal the other players are, your goal is to deduce it using the context they provide.
Starting with "I" describe yourself in 10 words or less as if you are the same animal as the other players. 
If no one else has said anything try to say something generic that could be true of any animals. 
If the other players realize you are the Chameleon you will LOSE. 
Previously Mentioned Descriptions:
{player_responses}
"""

_vote_prompt = """\
Below are the responses from all players. Now it is time to vote. Choose from the players below who you think the Chameleon is.
{player_responses}
"""

prompts = {
    "herd_animal": _game_rules + _herd_animal,
    "chameleon_animal": _game_rules + _chameleon_animal,
    "vote": _vote_prompt
}

