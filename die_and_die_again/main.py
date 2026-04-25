from argparse import ArgumentParser
import logging
import sys
from traceback import format_exc


from constants import __app_name__, app_info_string
from core.log_utils import setup_logger
from core.game_utils import random_first_name
from core.chance_calculator import ChanceCalculator
from core.die import DieType, DieRollWorker, DieWeightsWorker
from core.game_die import GameDieFactory
from core.player import PlayerBase
from core.game import GamePlayer, Game
from core.dice_games import OddEvenRoundType, OddEvenPlayer, OddEvenGame
from app import DieApp

logger = logging.getLogger(__app_name__)


def run_die_sandpit():
    logger.info("Die Sandbox")

    die_1 = GameDieFactory.random_die(die_type=DieType.D6)
    die_2 = GameDieFactory.random_die(die_type=DieType.D6)
    die_3 = GameDieFactory.random_die(die_type=DieType.D6)
    die_4 = GameDieFactory.random_die(die_type=DieType.D4)
    die_5 = GameDieFactory.random_die(die_type=DieType.D12)

    all_dice = [die_1, die_2, die_3, die_4, die_5]
    die_names = [
        "Die 1",
        "Die 2 (O\u2191)",
        "Die 3 (E\u2191)",
        "Lucky 4(4\u2191)",
        "#5 12s",
    ]

    DieWeightsWorker(die_2).adjust_weights([(1, 200.0), (3, 250.0), (5, 300.0)])
    DieWeightsWorker(die_3).adjust_weights([(2, 200.0), (4, 250.0), (6, 300.0)])
    DieWeightsWorker(die_4).adjust_weights(
        [
            (4, 400.0),
        ]
    )

    line_length = 120
    num_rolls = 100000
    num_rolls_len = len(str(num_rolls))

    for die, name in zip(all_dice, die_names):
        sys.stdout.flush()
        sys.stdout.write(f"{str('~' * line_length)}\n{name} Rolls: {num_rolls}\n")

        for i in range(num_rolls):
            value = die.roll()
            if i % 100 == 0 or i == num_rolls - 1:
                text = f"{str(i + 1).ljust(num_rolls_len).rjust(num_rolls_len)}/{num_rolls} [{value}]"
                sys.stdout.write(f"\r{text.ljust(line_length)}")
                sys.stdout.flush()

        sys.stdout.write("\r" + str(" " * line_length))
        sys.stdout.flush()

        roll_data = DieRollWorker(die).calculate_deviations_from_average()
        roll_data.sort_lists_by_value()

        def write_values(vals, title):
            log_values = " ".join([f"{v:1d}: {w:.3f}" for v, w in vals])
            sys.stdout.write(f"{title.rjust(14)}: {log_values}\n")

        sys.stdout.write(
            f"\rAvg ratio: {roll_data.avg_ratio:.3f}, Avg devtn: {roll_data.avg_deviation:.3f}\n"
        )
        write_values(roll_data.roll_ratios, "Roll Ratios")
        write_values(roll_data.deviations, "Deviations")
        sys.stdout.write(str("=" * line_length) + "\n")


def run_odds_evens_game():
    logger.info("Odds and Evens")

    def player_text(ply: OddEvenPlayer):
        return f"{ply.player.name.rjust(10)} ${ply.player.cash:4d}: score:{ply.score:3d} [{','.join([str(d) for d in ply.dice])}]"

    def create_npc(dice_ref: list, cash: int = 0):
        npc_player = PlayerBase(f"{random_first_name()} (NPC)", cash)
        npc_player.add_dice(GameDieFactory.dice_group(dice_ref))
        return npc_player

    dice_types = [
        (DieType.D6, 5),
    ]
    # dice_types = [(DieType.D3, 1), (DieType.D4, 2), (DieType.D6, 2)]

    player = Game.default_player()
    player_dice, player_missing = player.get_dice_group(dice_types)
    if player_missing:
        raise ValueError(f"Player Missing Dice: {player_missing}")

    # Weighting upgrade for Player
    for d in player_dice:
        d.change_weighting(6, 300.0)
        d.change_weighting(5, 300.0)

    npc_player = create_npc(dice_types, cash=100)
    npc_dice, npc_missing = npc_player.get_dice_group(dice_types)
    if npc_missing:
        raise ValueError(f"NPC Missing Dice: {npc_missing}")

    ply_1 = OddEvenPlayer(player, dice=player_dice)
    ply_2 = OddEvenPlayer(npc_player, dice=npc_dice)

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
            winner_text = f"Winner {winner.player.name}"
            wins[winner] += 1
        logger.info(f"Game {game_num}: {winner_text} : {score[0]} - {score[1]}")

    wins = sorted(
        [(key, value) for key, value in wins.items()], key=lambda p: p[1], reverse=True
    )
    wins_text = ", ".join([f"{w[0].player.name} ({w[1]})" for w in wins])
    logger.info(f"Winner: {wins_text}")


def chance_sandpit():
    logger.info("Chance Sandpit")

    denom = 10
    chance = ChanceCalculator(1 / denom)

    for i in range(10):
        count = 0
        while True:
            count += 1
            if chance.roll():
                break
        logger.info(f"{i + 1}: Rolled {count} times for 1/{denom} chance.")


def run_main_game():
    game = Game.default_game("Dwayne")
    # game_seed = 19790918
    # game = Game.seeded_game(game_seed)

    logger.info(f"Starting Game: {game}")


def main(app_args):
    setup_logger(__app_name__)
    logger.setLevel(logging.DEBUG if app_args.verbose else logging.INFO)
    logger.info(app_info_string())
    logger.info(
        f"[loglvl={logging.getLevelName(logger.getEffectiveLevel())}]Starting..."
    )

    if app_args.gui:
        app = DieApp(sys.argv)
        sys.exit(app.run())

    try:
        run_die_sandpit()
        # run_odds_evens_game()
        # chance_sandpit()
        run_main_game()

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
