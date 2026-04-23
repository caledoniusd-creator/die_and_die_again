from enum import Enum, unique
from functools import cache

import logging


from constants import __app_name__
from .game import PlayerBase

logger = logging.getLogger(__app_name__)


@unique
class OddEvenRoundType(Enum):
    Odds = 1
    Evens = 2
    Final = 3

    @staticmethod
    def round_list(num_rounds: int = 2):
        rounds = []
        for _ in range(num_rounds):
            rounds.extend([OddEvenRoundType.Odds, OddEvenRoundType.Evens])
        rounds.append(OddEvenRoundType.Final)
        return rounds


class OddEvenPlayer:
    def __init__(self, player: PlayerBase, dice: list | None = None):
        self._player = player
        self._dice = dice if dice is not None else []
        self._score = 0

    @property
    def player(self):
        return self._player

    # @property
    # def name(self):
    #     return self.player.name

    # @property
    # def cash(self):
    #     return self.player.cash

    @property
    def dice(self):
        return self._dice

    @property
    def score(self):
        return self._score

    def add_score(self, score: int):
        self._score += score

    def reset_score(self):
        self._score = 0


class OddEvenGame:
    @staticmethod
    def roll_values_text(rolls: list):
        return f"[{','.join([str(r) for r in rolls])}]"

    def __init__(
        self,
        player_1: OddEvenPlayer,
        player_2: OddEvenPlayer,
        rounds: list[OddEvenRoundType],
    ):
        self._player_1 = player_1
        self._player_2 = player_2
        self._rounds = rounds
        self._current_round = 0

    @property
    def player_1(self):
        return self._player_1

    @property
    def player_2(self):
        return self._player_2

    @cache
    def players(self):
        return [self._player_1, self._player_2]

    @property
    def rounds(self):
        return self._rounds

    @property
    def current_round(self):
        return self._current_round

    def has_finished(self):
        return self._current_round > len(self._rounds) - 1

    def play_round(self):
        if self.has_finished():
            logger.info("Game Finished!")
            return

        round_type = self._rounds[self._current_round]
        round_text = f"Round: {round_type.name.ljust(5)} : "

        round_scores = []
        for player in self.players():
            ply_rolls = [d.roll() for d in player.dice]
            if round_type == OddEvenRoundType.Odds:
                ply_vrolls = [r for r in ply_rolls if r % 2 == 1]
            elif round_type == OddEvenRoundType.Evens:
                ply_vrolls = [r for r in ply_rolls if r % 2 == 0]
            else:
                ply_vrolls = ply_rolls

            round_score = sum(ply_vrolls)
            if round_type == OddEvenRoundType.Final:
                round_score *= 2
            player.add_score(round_score)
            round_scores.append((round_score, ply_vrolls))

        for player, round_score in zip(self.players(), round_scores):
            pscore_t = f"{player.score}"
            score_t = f"{str(round_score[0]).rjust(len(pscore_t))}/{pscore_t}"
            text = f"{player.player.name.rjust(10)}:{OddEvenGame.roll_values_text(round_score[1]).rjust(16)} ({score_t})"
            if player == self.player_1:
                round_text += text.ljust(40)
            else:
                round_text += " - " + text.ljust(40)
        logger.info(round_text)
        self._current_round += 1

    def winner(self):
        tmp_players = sorted(self.players(), key=lambda p: p.score, reverse=True)
        winner = (
            tmp_players[0] if tmp_players[0].score != tmp_players[1].score else None
        )
        return winner, (tmp_players[0].score, tmp_players[1].score)

    def reset(self):
        for player in self.players():
            player.reset_score()
        self._current_round = 0
