# heavily inspired by: https://github.com/bitcraft/pyscroll/blob/master/apps/demo/demo.py
import logging

import pygame

from game import Game
from utils import init_screen

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def main_cli():
    import sys

    pygame.init()
    pygame.font.init()
    screen = init_screen(800, 800)
    pygame.display.set_caption("Shifumi")

    try:
        filename = sys.argv[1]
    except IndexError:
        logger.info("no TMX map specified, using default")
        filename = "resources/carte.tmx"

    try:
        test = Game(filename, screen)
        test.run()
    except:
        pygame.quit()
        raise


if __name__ == "__main__":
    main_cli()
