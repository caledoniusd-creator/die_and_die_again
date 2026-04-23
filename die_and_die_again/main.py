from argparse import ArgumentParser
from enum import Enum, unique
from functools import cache
import logging
import sys
from traceback import format_exc


from constants import __app_name__, app_info_string
from core.log_utils import setup_logger
from core.game_utils import random_first_name
from core.chance_calculator import ChanceCalculator
from core.die import DieType
from core.game_die import GameDieFactory
from core.game import GamePlayer, Game
from core.dice_games import OddEvenRoundType, OddEvenPlayer, OddEvenGame
from app import DieApp

logger = logging.getLogger(__app_name__)


def run_die_sandpit():
    logger.info("Die Sandbox")

    # game
    player = GamePlayer.default_player()
    game = Game(player=player)
    logger.info(f"New Game: {game}")
    logger.info(
        f"#Boxes={player.num_boxes}, #Shakers={player.num_shakers}, #Dice={player.total_num_dice()}"
    )

    dice_text = "[" + ", ".join([str(d) for d in player.all_dice()]) + "]"
    logger.info(f"Dice: {dice_text}")

    dice_group = [GameDieFactory.random_die(die_type=DieType.D6) for _ in range(5)]

    all_rolls = []
    for _ in range(4):
        rolls = [d.roll() for d in dice_group]

        rolls_text = ", ".join([str(r) for r in rolls])
        logger.info(f"Rolls: [{rolls_text}]")
        all_rolls.append(rolls)

    totals = [sum(r) for r in all_rolls]
    full_total = sum(totals)

    logger.info(f"Totals: {totals}, full: {full_total}")


def run_odds_evens_game():
    logger.info("Odds and Evens")

    def player_text(ply:OddEvenPlayer):
        return f"{ply.name.rjust(10)} ${ply.cash:4d}: score:{ply.score:3d} [{','.join([str(d) for d in ply.dice])}]"

    dice_types = [(DieType.D6, 5),]
    # dice_types = [(DieType.D3, 1), (DieType.D4, 2), (DieType.D6, 2)]

    ply_1 = OddEvenPlayer(random_first_name(), dice=GameDieFactory.dice_group(dice_types))
    ply_2 = OddEvenPlayer(random_first_name(), dice=GameDieFactory.dice_group(dice_types))

    for player in [ply_1, ply_2]:
        logger.info(player_text(player))

    num_games = 5
    # valid odd number of games
    num_games += 1 if num_games % 2 == 0 else 0

    game = OddEvenGame(ply_1, ply_2, OddEvenRoundType.round_list(num_rounds=2))
    wins = {ply: 0 for ply in [ply_1, ply_2]}
    for game_num in range(1, num_games + 1):
        game.reset()
        while not game.has_finished():
            game.play_round()
        winner, score = game.winner()
        if winner is None:
            winner_text = "Tied!"
        else:
            winner_text = f"Winner {winner.name}"
            wins[winner] += 1
        logger.info(f"Game {game_num}: {winner_text} : {score[0]} - {score[1]}")

    wins = sorted([(key, value) for key, value in wins.items()], key=lambda p: p[1], reverse=True)
    wins_text = ", ".join([f"{w[0].name} ({w[1]})" for w in wins])
    logger.info(f"Winner: {wins_text}")


def chance_sandpit():
    logger.info("Chance Sandpit")

    denom = 10
    chance = ChanceCalculator(1/denom)

    for i in range(10):
        count = 0
        while True:
            count += 1
            if chance.roll():
                break
        logger.info(f"{i+1}: Rolled {count} times for 1/{denom} chance.")


def main(args):
    setup_logger(__app_name__)
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    logger.info(app_info_string())
    logger.info(
        f"[loglvl={logging.getLevelName(logger.getEffectiveLevel())}]Starting..."
    )

    if args.gui:
        app = DieApp(sys.argv)
        sys.exit(app.run())

    try:
        # run_die_sandpit()
        # run_odds_evens_game()
        chance_sandpit()

    except Exception as e:
        logger.debug(format_exc())
        logger.exception(e)
        logger.error(str(e))


if __name__ == "__main__":
    parser = ArgumentParser("die_and_die_again")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="More verbose logging.",
    )
    parser.add_argument(
        "-g", "--gui", action="store_true", default=False, help="Running GUI mode"
    )
    args = parser.parse_args()

    main(args)
