import os
import sys

import pygame

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphics.image_handler import Image_Handler
from graphics.special_screens.main_screen import Main_Screen
from graphics.special_screens.credits import Credits_Screen


class Game_State:
    """
    Register per-state update logic with
      register_state(), and switch state (and the matching scene) with
      change_state().
    self.image_handler is the single Image_Handler instance used for
      everything drawn on screen.
    """

    def __init__(self, width=1280, height=720, title="Game"):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))

        self.image_handler = Image_Handler(self.screen)

        self.running = False
        self.state = "menu"
        self.states = {}  # name -> callable(dt), run every frame while active

        self._setup_scenes()

    def _setup_scenes(self):
        """Register the initial set of scenes. More scenes (and entities
        within them) can be added later at any time via
        self.image_handler.add_scene(...) / add_entity_to_scene(...).
        """
        main_screen = Main_Screen(self.image_handler)
        credit_screen = Credits_Screen(self.image_handler)

        self.image_handler.add_scene(main_screen)
        self.image_handler.add_scene(credit_screen)


    def register_state(self, name, update_callback):
        """
        Attach game-logic that should run every frame while `name` is
        the active state
        For Example:
        game.register_state("playing", world.update)
        """
        self.states[name] = update_callback

    def change_state(self, name, fade=True):
        """Switch both the logical game state and the graphical scene (if
        a scene with a matching name is registered).
        """
        self.state = name
        if name in self.image_handler.scenes:
            self.image_handler.set_scene(name, fade=fade)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # let the active scene react to input
            scene = self.image_handler.current_scene
            if scene is not None and hasattr(scene, "handle_event"):
                scene.handle_event(event)

    def update(self, dt):
        self.image_handler.update(dt)

        update_callback = self.states.get(self.state)
        if update_callback is not None:
            update_callback(dt)

    def draw(self):
        self.image_handler.draw()

    def run(self):
        """Blocking call, runs the game loop at a fixed 60 FPS until
        something sets self.running = False
        """
        self.running = True
        while self.running:
            dt = self.image_handler.tick()
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
