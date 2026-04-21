from argparse import ArgumentParser
import logging
import sys
from traceback import format_exc


from constants import APP_NAME
from core.die import DieType
from core.game_die import DieMaterial, GameDie, GameDieFactory

logger = logging.getLogger(APP_NAME)


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
    die_type = DieType.D6

    game_die = GameDieFactory.new_die(die_type.sides)
    logger.info(
        "\n".join(
            [
                f"Game Die ({die_type}):",
            ]
            + [" - " + it for it in game_die.info_text()]
        )
    )


def main(args):
    setup_logger(APP_NAME)
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    logger.info(f"[loglvl={logging.getLevelName(logger.getEffectiveLevel())}]Starting {APP_NAME}...")

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
    # parser.add_argument(
    #     "-g", "--gui", action="store_true", default=True, help="Running GUI mode"
    # )
    args = parser.parse_args()

    main(args)
