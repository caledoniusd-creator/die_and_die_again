from argparse import ArgumentParser
import logging
import sys
from traceback import format_exc


from constants import __app_name__, app_info_string
from core.die import DieType
from core.game_die import DieMaterial, GameDie, GameDieFactory
from core.game import GamePlayer, Game
from app import DieApp

logger = logging.getLogger(__app_name__)


def setup_logger(logger_name: str = ""):
    """
    Sets up a logger with a specific name and configuration.

    This function initializes and configures a logger instance with a provided name.
    The logger is configured to stream messages to the standard output using a specific
    log format. Useful for consistent logging across various modules.

    :param logger_name: The name of the logger to set up. If not provided, the root logger is used.
    :type logger_name: str
    :return: A configured logger instance.
    :rtype: logging.Logger
    """
    log_formatter = logging.Formatter(
        "%(asctime)s |%(levelname)s|%(funcName)s:%(lineno)d| %(message)s"
    )
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_formatter)

    logger_edit = logging.getLogger(logger_name)
    logger_edit.addHandler(log_handler)


def run_die_sandpit():
    logger.info("Die Sandbox")

    # die_type = DieType.random()
    # die_type = DieType.D6

    # game_die = GameDieFactory.new_die(die_type.sides)
    # logger.info(f"New Die: {game_die}")

    # game
    player = GamePlayer.default_player()
    game = Game(player=player)
    logger.info(f"New Game: {game}")
    logger.info(f"#Boxes={player.num_boxes}, #Shakers={player.num_shakers}, #Dice={player.total_num_dice()}")

    dice_text = "[" + ", ".join([str(d) for d in player.all_dice()]) + "]"
    logger.info(f"Dice: {dice_text}")

    dice_group = [
        GameDieFactory.random_die(die_type=DieType.D6) for _ in range(5)
    ]

    all_rolls = []
    for _ in range(4):
        rolls = [d.roll() for d in dice_group]

        rolls_text = ", ".join([str(r) for r in rolls])
        logger.info(f"Rolls: [{rolls_text}]")
        all_rolls.append(rolls)

    totals = [sum(r) for r in all_rolls]
    full_total = sum(totals)

    logger.info(f"Totals: {totals}, full: {full_total}")


def main(args):
    setup_logger(__app_name__)
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    logger.info(app_info_string())
    logger.info(f"[loglvl={logging.getLevelName(logger.getEffectiveLevel())}]Starting...")

    if args.gui:
        app = DieApp(sys.argv)
        sys.exit(app.run())

    try:
        run_die_sandpit()

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
