import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

Additional functions are made available by importing the AdvancedGameState
class from gamelib/advanced.py as a replcement for the regular GameState class
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical
board states. Though, we recommended making a copy of the map to preserve
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    def starter_strategy(self, game_state):
        """
        Each player begins the game with 25 Cores, 5 Bits, and 30 Health
        """

        self.build_basic_defense(game_state)
        self.deploy_attackers(game_state)

    def build_basic_defense(self, game_state):

        destructor_locations_EW_edges = [
            [2, 11], [9, 10], [19, 10], [25, 11],
        ]

        filter_locations_EW_edges = [
            [0, 13], [27,13],
            [1, 12], [2, 12], [3, 12], [25, 12], [26, 12], [24, 12],
        ]

        if(self.check_for_damage, [destructor_locations_EW_edges, filter_locations_EW_edges]):
            self.build(game_state, DESTRUCTOR, destructor_locations_EW_edges)
            self.build(game_state, FILTER, filter_locations_EW_edges)


    def build_defense(self, game_state):

        firewall_locations = [
            [3, 12], [10, 12], [17, 12], [24, 12],
        ]

        filter_locations = [
            [2, 13], [3, 13], [4, 13],
            [9, 13], [10,13], [11, 13],
            [16, 13], [17, 13], [18, 13],
            [23, 13], [24, 13], [25, 13],
        ]

        self.build(game_state, ENCRYPTOR, firewall_locations)
        self.build(game_state, FILTER, filter_locations)

    def deploy_attackers(self, game_state):
        if(game_state.get_resource(game_state.BITS) < 10):
            return

        if(game_state.can_spawn(EMP, [3, 10])):
            game_state.attempt_spawn(EMP, [3, 10])

    def build(self, game_state, UNIT, locations):
        for location in locations:
         if game_state.can_spawn(UNIT, location):
             game_state.attempt_spawn(UNIT, location)

    def check_for_damage(self, game_state, defense_list):
        """
        checks if a list of given structures contains defense.
        returns: true if no structure is present.
        """
        for locations in defense_list:
            for location in locations:
                if(game_state.contains_stationary_unit):
                    return True


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
