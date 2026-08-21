import pygame

from graphics.assets import AssetManager
from graphics.scene import SceneManager
from game_logic.game_data import GameData
from graphics.special_screens.main_menu_screen import MainMenuScreen
from graphics.special_screens.credits import CreditsScreen


class GameApp:

    def __init__(self, width=1280, height=720, title="Game", fps=60):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.assets = AssetManager() #loading and caching images/spritesheets
        self.scenes = SceneManager(self.screen)
        self.game_data = GameData()  # party, gold, inventory transferred when switching screens

        self.running = False
        self.mode = "menu"
        self._mode_updates = {}  # mode name -> callable(dt), run every frame while active

        self._setup_screens()

    def _setup_screens(self):
        """Register the initial set of screens. More screens (Combat,
        Level Up...) get added here the same way later on.
        """
        self.scenes.add_scene(MainMenuScreen(self))
        self.scenes.add_scene(CreditsScreen(self))

    def register_mode(self, name, update_callback):
        """Attach per-frame game logic that should run while `name` is
        the active mode
        For Example:
        game.register_mode("playing", world.update)
        """
        self._mode_updates[name] = update_callback

    def change_mode(self, name, fade=True):
        """Switch both the logical game mode and the matching scene (if
        one is registered under the same name).
        """
        self.mode = name
        if name in self.scenes.scenes:
            self.scenes.set_scene(name, fade=fade)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # let the active scene react to input
            scene = self.scenes.current_scene
            if scene is not None and hasattr(scene, "handle_event"):
                scene.handle_event(event)

    def update(self, dt):
        self.scenes.update(dt)

        update_callback = self._mode_updates.get(self.mode)
        if update_callback is not None:
            update_callback(dt)

    def draw(self):
        self.scenes.draw()

    def get_fps(self):
        return self.clock.get_fps()

    def run(self):
        """Blocking call, runs the game loop at a fixed FPS until
        something sets self.running = False.
        """
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
