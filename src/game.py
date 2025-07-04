import collections
from typing import Deque

import pygame
import pyscroll
import pyscroll.data
import pyscroll.orthographic
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT, VIDEORESIZE
from pytmx.util_pygame import load_pygame

from utils import init_screen

SCROLL_SPEED = 5000


class Game:
    """Test and demo of pyscroll

    For normal use, please see the quest demo, not this.

    """

    def __init__(self, filename, screen) -> None:
        self.screen = screen
        # load data from pytmx
        tmx_data = load_pygame(filename)

        # create new data source
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        # create a font and pre-render some text to be displayed over the map
        f = pygame.font.Font(pygame.font.get_default_font(), 20)
        t = ["Shifumi demo. press escape to quit", "arrow keys move"]

        # save the rendered text
        self.text_overlay = [f.render(i, 1, (180, 180, 0)) for i in t]

        # set our initial viewpoint in the center of the map
        self.center = [
            self.map_layer.map_rect.width / 2,
            self.map_layer.map_rect.height / 2,
        ]

        # the camera vector is used to handle camera movement
        self.camera_acc: list[float] = [0, 0, 0]
        self.camera_vel: list[float] = [0, 0, 0]
        self.last_update_time = 0

        # true when running
        self.running = False

    def draw(self, surface) -> None:
        # tell the map_layer (BufferedRenderer) to draw to the surface
        # the draw function requires a rect to draw to.
        self.map_layer.draw(surface, surface.get_rect())

        # blit our text over the map
        self.draw_text(surface)

    def draw_text(self, surface) -> None:
        y = 0
        for text in self.text_overlay:
            surface.blit(text, (0, y))
            y += text.get_height()

    def handle_input(self) -> None:
        """Simply handle pygame input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

        # these keys will change the camera vector
        # the camera vector changes the center of the viewport,
        # which causes the map to scroll

        # using get_pressed is slightly less accurate than testing for events
        # but is much easier to use.
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.camera_acc[1] = -SCROLL_SPEED * self.last_update_time
        elif pressed[K_DOWN]:
            self.camera_acc[1] = SCROLL_SPEED * self.last_update_time
        else:
            self.camera_acc[1] = 0

        if pressed[K_LEFT]:
            self.camera_acc[0] = -SCROLL_SPEED * self.last_update_time
        elif pressed[K_RIGHT]:
            self.camera_acc[0] = SCROLL_SPEED * self.last_update_time
        else:
            self.camera_acc[0] = 0

    def update(self, td) -> None:
        self.last_update_time = td

        friction = pow(0.0001, self.last_update_time)

        # update the camera vector
        self.camera_vel[0] += self.camera_acc[0] * td
        self.camera_vel[1] += self.camera_acc[1] * td

        self.camera_vel[0] *= friction
        self.camera_vel[1] *= friction

        # make sure the movement vector stops when scrolling off the screen
        if self.center[0] < 0:
            self.center[0] -= self.camera_vel[0]
            self.camera_acc[0] = 0
            self.camera_vel[0] = 0
        if self.center[0] >= self.map_layer.map_rect.width:
            self.center[0] -= self.camera_vel[0]
            self.camera_acc[0] = 0
            self.camera_vel[0] = 0

        if self.center[1] < 0:
            self.center[1] -= self.camera_vel[1]
            self.camera_acc[1] = 0
            self.camera_vel[1] = 0
        if self.center[1] >= self.map_layer.map_rect.height:
            self.center[1] -= self.camera_vel[1]
            self.camera_acc[1] = 0
            self.camera_vel[1] = 0

        self.center[0] += self.camera_vel[0]
        self.center[1] += self.camera_vel[1]

        # set the center somewhere else
        # in a game, you would set center to a playable character
        self.map_layer.center(self.center)

    def run(self) -> None:
        clock = pygame.time.Clock()
        self.running = True
        fps = 60.0
        fps_log: Deque[float] = collections.deque(maxlen=20)

        try:
            while self.running:
                # somewhat smoother way to get fps and limit the framerate
                clock.tick(fps * 2)

                try:
                    fps_log.append(clock.get_fps())
                    fps = sum(fps_log) / len(fps_log)
                    dt = 1 / fps
                except ZeroDivisionError:
                    continue

                self.handle_input()
                self.update(dt)
                self.draw(self.screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False
