import pygame
import pytmx
import pyscroll
import pytmx.util_pygame

class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Shifumi")

        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):
         
        running = True

        while running:

            self.group.draw(self.screen)
            pygame.display.flip

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit