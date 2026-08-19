"""
Central place for everything image / graphics related

Nothing in here depends on any specific game logic, Game_State (in
game_logic/game_state.py) is what ties this to the rest of the game.
"""

import os
import pygame


class Animation:
    """
    Frame can be build with:
    Image_Handler.load_image / load_spritesheet / make_animation.
    """

    def __init__(self, frames, frame_duration=0.1, loop=True):
        """
        frames: list[pygame.Surface] = the individual animation frames
        frame_duration: seconds each frame is shown for
        loop: animation restarts after the last frame,
              or freezes on the last frame once finished
        """
        if not frames:
            raise ValueError("Animation needs at least one frame")

        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self._timer = 0.0
        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        self._timer += dt
        while self._timer >= self.frame_duration:
            self._timer -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def reset(self):
        self.current_frame = 0
        self._timer = 0.0
        self.finished = False

    def get_current_frame(self):
        return self.frames[self.current_frame]


class Drawable:
    """Wraps a static image OR an animation together with a position, so
    it can be added to a scene as a single drawable: a player sprite, an
    item...
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
    """A container for everything that should be shown at once (a title
    screen, a menu, a level, ...).

    Meant to be used directly for simple cases, or subclassed for scenes
    that need custom behaviour. Image_Handler only ever calls .update(dt) and
    .draw(surface) aswell as .on_enter()/.on_exit() on scene switches, so any
    object implementing that interface works as a scene.
    """

    def __init__(self, name, background=None):
        self.name = name
        self.background = background  # pygame.Surface or None
        self.drawables:list[Drawable] = []  # list[Drawable], kept sorted by layer

    def add_drawable(self, drawable):
        """Add a new drawable object to this scene at runtime,
        e.g. for a newly spawned entity.
        """
        self.drawables.append(drawable)
        self.drawables.sort(key=lambda drawable_: drawable_.layer)

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


class Image_Handler:
    """Central image/graphics manager.
    """

    FPS = 60

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self._image_cache = {}
        self.scenes = {}
        self.current_scene = None

        # fade transition state (used by set_scene(..., fade=True))
        self._fade_state = None  # None, "out" or "in"
        self._fade_alpha = 0
        self._fade_speed = 500  # alpha units per second
        self._fade_pending_scene = None
        self._fade_surface = pygame.Surface(self.screen.get_size())
        self._fade_surface.fill((0, 0, 0))

    def load_image(self, path, scale=None, colorkey=None, use_alpha=True):
        """Load an image from disk, caching it so repeated loads are free after the first time.

        path: file path to the image
        scale: optional (width, height) to resize the image to
        colorkey: optional RGB color to treat as transparent
        use_alpha: convert_alpha() vs convert(), use False for opaque
                   backgrounds
        """
        cache_key = (path, scale, colorkey, use_alpha)
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        if not os.path.exists(path):
            raise FileNotFoundError(f"Image_Handler: could not find image '{path}'")

        image = pygame.image.load(path)
        image = image.convert_alpha() if use_alpha else image.convert()

        if colorkey is not None:
            image.set_colorkey(colorkey)

        if scale is not None:
            image = pygame.transform.scale(image, scale)

        self._image_cache[cache_key] = image
        return image

    def load_drawable(self, path,name, pos=(0,0),visible=True, layer=0, scale=None, colorkey=None, use_alpha=True):
        """Load an image from disk, caching it so repeated loads are free after the first time.

        path: file path to the image
        scale: optional (width, height) to resize the image to
        colorkey: optional RGB color to treat as transparent
        use_alpha: convert_alpha() vs convert(), use False for opaque
        backgrounds
        """
        image = self.load_image(path,scale,colorkey,use_alpha)
        drawable = Drawable(name,image=image,animation=None,pos=pos,visible=visible,layer=layer)
        return drawable


    def load_spritesheet(self, path, frame_width, frame_height, num_frames, scale=None):
        """Slice a horizontal spritesheet into a list of frame Surfaces,
        used for building an Animation with make_animation() or directly.
        """
        sheet = self.load_image(path)
        frames = []
        for i in range(num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sheet.subsurface(rect).copy()
            if scale is not None:
                frame = pygame.transform.scale(frame, scale)
            frames.append(frame)
        return frames

    def clear_cache(self):
        self._image_cache.clear()

    def add_scene(self, scene):
        """Register a new scene.
          The first scene added automatically becomes active.
        """
        self.scenes[scene.name] = scene
        if self.current_scene is None:
            self.current_scene = scene
            self.current_scene.on_enter()

    def set_scene(self, name, fade=False, fade_speed=500):
        """Switch the active scene by name.

        fade=True plays a quick fade to black transition instead
        of switching instantly.
        """
        if name not in self.scenes:
            raise KeyError(f"Image_Handler: no scene registered under '{name}'")

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
        """Add a new Drawable to a specific
        scene, whether or not it's currently active.
        """
        scene = self.get_scene(scene_name)
        if scene is None:
            raise KeyError(f"Image_Handler: no scene registered under '{scene_name}'")
        scene.add_drawable(drawable)

    def add_drawable_to_current_scene(self, drawable):
        if self.current_scene is None:
            raise RuntimeError("Image_Handler: no active scene to add an drawable to")
        self.current_scene.add_drawable(drawable)


    def make_animation(self, image_paths, frame_duration=0.1, loop=True, scale=None):
        """build an Animation straight from a list of image
        file paths (each one loaded/cached through load_image).
        """
        frames = [self.load_image(p, scale=scale) for p in image_paths]
        return Animation(frames, frame_duration=frame_duration, loop=loop)


    def tick(self):
        """Advance the clock, capping the loop at FPS (60 by default), and
        return the elapsed time in seconds (dt). Call exactly once per
        frame, before update()/draw().
        """
        return self.clock.tick(self.FPS) / 1000.0

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

    def get_fps(self):
        return self.clock.get_fps()