from argparse import ArgumentParser
import logging


def main(args):
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        )
    

if __name__ == "__main__":

    parser = ArgumentParser("die_and_die_again")
    parser.add_argument(
        "-g", "--gui", action="store_true", default=True, help="Running GUI mode"
    )
    args = parser.parse_args()

    main(args)

