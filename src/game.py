from prompts import fetch_prompt
from player import Player


class Game:
    def __init__(self):
        print("Game Created")
        self.players = []

    def add_players(self, players: list[Player]):
        """Adds players to the game."""
        self.players = players

    def broadcast(self, message):
        """Sends a message to all the players, no response required."""
        for player in self.players:
            player.add_message(message)

    def format_responses(self, responses: list[str]) -> str:
        """Formats the responses of the players into a single string."""
        return "\n".join(responses)

    def start(self):
        """Starts the game."""
        print("Welcome to Chameleon! This is a social deduction game powered by LLMs.")

        if not self.players:
            print("Enter your name to begin")
            human_name = input()

            self.add_players([
                Player("Player 1", "ai", "herd"),
                Player("Player 2", "ai", "herd"),
                Player("human_name", "human", "chameleon"),
                Player("Player 4", "ai", "herd"),
                Player("Player 5", "ai", "herd")
            ])

        self.player_responses = []
        herd_animal = "Giraffe"

        # Collect Player Animal Descriptions
        for player in self.players:
            match player.role:
                case "herd":
                    prompt_template = fetch_prompt("herd_animal")
                    prompt = prompt_template.format(animal=herd_animal, player_responses=self.player_responses)

                case "chameleon":
                    prompt_template = fetch_prompt("chameleon_animal")
                    prompt = prompt_template.format(player_responses="")

            response = player.collect_input(prompt)
            self.player_responses.append(response)

        self.player_votes = []

        # Collect Player Votes
        for player in self.players:
            prompt_template = fetch_prompt("vote")
            prompt = prompt_template.format(animal=herd_animal, player_responses=self.player_responses)

            response = player.collect_input(prompt)
            self.player_responses.append(response)



