"""
Loading and caching of images and spritesheets.
"""

import os
import pygame

from graphics.animation import Animation
from graphics.scene import Drawable


class AssetManager:

    def __init__(self):
        self._image_cache = {}

    def load_image(self, path, scale=None, colorkey=None, use_alpha=True):
        """
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
            raise FileNotFoundError(f"AssetManager: could not find image '{path}'")

        image = pygame.image.load(path)
        image = image.convert_alpha() if use_alpha else image.convert()

        if colorkey is not None:
            image.set_colorkey(colorkey)

        if scale is not None:
            image = pygame.transform.scale(image, scale)

        self._image_cache[cache_key] = image
        return image

    def load_drawable(self, path, name, pos=(0, 0), visible=True, layer=0,
                       scale=None, colorkey=None, use_alpha=True):
        """Load an image and wrap it in a Drawable.
        """
        image = self.load_image(path, scale, colorkey, use_alpha)
        return Drawable(name, image=image, pos=pos, visible=visible, layer=layer)

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

    def make_animation(self, image_paths, frame_duration=0.1, loop=True, scale=None):
        """Build an Animation straight from a list of image file paths
        (each one loaded/cached through load_image).
        """
        frames = [self.load_image(p, scale=scale) for p in image_paths]
        return Animation(frames, frame_duration=frame_duration, loop=loop)

    def clear_cache(self):
        self._image_cache.clear()
