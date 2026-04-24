from enum import Enum, unique
import logging
from random import randint, shuffle, seed as rng_seed

from constants import __app_name__

from .die import DieType
from .game_die import GameDie, GameDieFactory
from .player import PlayerBase
from .game_utils import reseed_faker, random_first_name

from .dice_box import DieBoxFullException, DiceBox

logger = logging.getLogger(__app_name__)


@unique
class DiceGod(Enum):
    Odds = ("Odds", 1)
    Evens = ("Evens", 2)
    Highs = ("Highs", 3)
    Lows = ("Lows", 4)



class GamePlayer(PlayerBase):
    def __init__(self, name: str, cash: int):
        super().__init__(name, cash)

    def __str__(self):
        return super().__str__()


class Game:

    @staticmethod
    def default_player(name: str|None=None, cash: int|None=None):
        player = GamePlayer(name or random_first_name(), cash or 200)
        # add Dice
        starting_dice = [
            (DieType.D4, 2), (DieType.D6, 5), (DieType.D20, 1),
        ]

        for dt in starting_dice:
            for _ in range(dt[1]):
                player.add_die(GameDieFactory.random_die(die_type=dt[0]))
        return player

    @staticmethod
    def default_game(player_name: str|None=None, cash: int=250):
        game = Game()
        player = Game.default_player(player_name, cash)
        game.player = player
        return game

    @staticmethod
    def seeded_game(game_seed: int, cash: int = 250):
        game = Game(game_seed=game_seed)
        player = Game.default_player(cash=cash)
        game.player = player
        return game

    def __init__(self, game_seed: int = 0):
        self._game_seed = game_seed if game_seed != 0 else randint(0, 0xFFFFFFFF)
        self._player = None
        rng_seed(self.game_seed)
        reseed_faker(self.game_seed)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player: GamePlayer):
        if not isinstance(player, GamePlayer):
            raise TypeError("player must be of type GamePlayer")
        self._player = player


    def __str__(self):
        return f"<{self.__class__.__name__} player=({self.player}), game_seed={hex(self.game_seed)}>"

    @property
    def game_seed(self):
        return self._game_seed
