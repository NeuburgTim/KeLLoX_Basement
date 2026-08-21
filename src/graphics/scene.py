"""
Scene/screen infrastructure: a Drawable wraps a sprite or animation with
a position, a Scene is a collection of Drawables shown together, and
SceneManager keeps track of which Scene is currently active, including
the fade transition between two scenes.
"""

import pygame


class Drawable:
    """A single visual object (player sprite, item icon, ...) with a
    position, that can be added to a Scene.
    """

    def __init__(self, name, image=None, animation=None, pos=(0, 0),
                 visible=True, layer=0):
        if image is None and animation is None:
            raise ValueError("Drawable needs either an image or an animation")

        self.name = name
        self.image = image
        self.animation = animation
        self.pos = list(pos)
        self.visible = visible
        self.layer = layer  # higher layer number = drawn on top

    def update(self, dt):
        if self.animation is not None:
            self.animation.update(dt)

    def get_surface(self):
        if self.animation is not None:
            return self.animation.get_current_frame()
        return self.image

    def draw(self, surface):
        if not self.visible:
            return
        surface.blit(self.get_surface(), self.pos)


class Scene:
    """Everything that should be shown at once: a title screen, a menu, a
    level, ... Subclass this for screens with custom behaviour (see
    ButtonScreen), or use it directly for very simple cases.

    SceneManager only ever calls update()/draw() and on_enter()/on_exit()
    when switching scenes, so anything implementing that interface works
    as a scene.
    """

    def __init__(self, name, background=None):
        self.name = name
        self.background = background  # pygame.Surface or None
        self.drawables: list[Drawable] = []  # kept sorted by layer

    def add_drawable(self, drawable):
        """Add a new drawable at runtime, e.g. for a newly spawned entity."""
        self.drawables.append(drawable)
        self.drawables.sort(key=lambda d: d.layer)

    def remove_drawable(self, name):
        self.drawables = [d for d in self.drawables if d.name != name]

    def get_drawable(self, name):
        for drawable in self.drawables:
            if drawable.name == name:
                return drawable
        return None

    def update(self, dt):
        for drawable in self.drawables:
            drawable.update(dt)

    def draw(self, surface):
        if self.background is not None:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((0, 0, 0))
        for drawable in self.drawables:
            drawable.draw(surface)

    def on_enter(self):
        """Called every time this scene becomes the active one."""
        pass

    def on_exit(self):
        """Called every time this scene stops being the active one."""
        pass


class SceneManager:
    """Owns every registered Scene and knows which one is active right
    now, including the fade-to-black transition between two scenes.
    """

    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

        # fade transition state (used by set_scene(..., fade=True))
        self._fade_state = None  # None, "out" or "in"
        self._fade_alpha = 0
        self._fade_speed = 500  # alpha units per second
        self._fade_pending_scene = None
        self._fade_surface = pygame.Surface(self.screen.get_size())
        self._fade_surface.fill((0, 0, 0))

    def add_scene(self, scene):
        """Register a new scene. The first one added becomes active."""
        self.scenes[scene.name] = scene
        if self.current_scene is None:
            self.current_scene = scene
            self.current_scene.on_enter()

    def set_scene(self, name, fade=False, fade_speed=500):
        """Switch the active scene by name. fade=True plays a quick fade
        to black instead of switching instantly.
        """
        if name not in self.scenes:
            raise KeyError(f"SceneManager: no scene registered under '{name}'")

        new_scene = self.scenes[name]

        if not fade:
            if self.current_scene is not None:
                self.current_scene.on_exit()
            self.current_scene = new_scene
            self.current_scene.on_enter()
            return

        self._fade_pending_scene = new_scene
        self._fade_speed = fade_speed
        self._fade_state = "out"

    def get_scene(self, name):
        return self.scenes.get(name)

    def add_drawable_to_scene(self, scene_name, drawable):
        """Add a Drawable to a specific scene, whether or not it's active."""
        scene = self.get_scene(scene_name)
        if scene is None:
            raise KeyError(f"SceneManager: no scene registered under '{scene_name}'")
        scene.add_drawable(drawable)

    def add_drawable_to_current_scene(self, drawable):
        if self.current_scene is None:
            raise RuntimeError("SceneManager: no active scene to add a drawable to")
        self.current_scene.add_drawable(drawable)

    def update(self, dt):
        if self.current_scene is not None:
            self.current_scene.update(dt)

        if self._fade_state == "out":
            self._fade_alpha += self._fade_speed * dt
            if self._fade_alpha >= 255:
                self._fade_alpha = 255
                if self.current_scene is not None:
                    self.current_scene.on_exit()
                self.current_scene = self._fade_pending_scene
                self.current_scene.on_enter()
                self._fade_pending_scene = None
                self._fade_state = "in"
        elif self._fade_state == "in":
            self._fade_alpha -= self._fade_speed * dt
            if self._fade_alpha <= 0:
                self._fade_alpha = 0
                self._fade_state = None

    def draw(self):
        if self.current_scene is not None:
            self.current_scene.draw(self.screen)

        if self._fade_alpha > 0:
            alpha = max(0, min(255, int(self._fade_alpha)))
            self._fade_surface.set_alpha(alpha)
            self.screen.blit(self._fade_surface, (0, 0))

        pygame.display.flip()
