"""
Generic base class for "background + title + a stack of buttons" screens.
"""

import pygame
from graphics.image_handler import Scene
from graphics.ui import Button, ButtonGroup


class Button_Screen(Scene):

    def __init__(self, name, image_handler, background_path=None,
                 title_text=None, title_font=None, title_color=(255, 255, 255),
                 title_pos=None, button_specs=(), button_size=(240, 60),
                 button_font=None, button_spacing=20):
        """
        name:            scene name, used by Image_Handler.set_scene()
        image_handler:   the shared Image_Handler instance
        background_path: optional path to a background image
        title_text:      optional heading drawn at the top of the screen
        title_pos:       defaults to horizontally centered, y=100
        button_specs:    iterable of (label, callback) tuples, or dicts
                          like {"label": ..., "callback": ..., "size": ...}
                          for per-button overrides (colors, size, font, ...)
        button_size:     default (w, h) for buttons that don't override it
        button_spacing:  vertical gap between stacked buttons
        """
        background = None
        if background_path:
            background = image_handler.load_image(
                background_path, scale=image_handler.screen.get_size()
            )
        super().__init__(name=name, background=background)

        self.image_handler = image_handler

        self.title_text = title_text
        self.title_font = title_font or (pygame.font.SysFont(None, 64) if title_text else None)
        self.title_color = title_color
        screen_w, _ = self.image_handler.screen.get_size()
        self.title_pos = title_pos or (screen_w // 2, 100)

        self.button_group = ButtonGroup()
        self._build_buttons(button_specs, button_size, button_font, button_spacing)

    def _build_buttons(self, button_specs, button_size, button_font, spacing):
        for spec in button_specs:
            if isinstance(spec, dict):
                spec = dict(spec) 
                label = spec.pop("label")
                callback = spec.pop("callback", None)
                size = spec.pop("size", button_size)
                font = spec.pop("font", button_font)
                extra_kwargs = spec  # anything left: bg_color, hover_color, ...
            else:
                label, callback = spec
                size = button_size
                font = button_font
                extra_kwargs = {}

            button = Button(label, pos=(0, 0), size=size, on_click=callback,
                             font=font, **extra_kwargs)
            self.button_group.add(button)

        self.button_group.layout_vertical_centered(
            self.image_handler.screen.get_size(), spacing=spacing
        )

    def get_button(self, label):
        """Look up a button by its text, e.g.:
        screen.get_button("Play").set_callback(...)
        """
        return self.button_group.get(label)

    def handle_event(self, event):
        """Image_Handler/Game_State should forward raw pygame events here"""
        self.button_group.handle_event(event)

    def update(self, dt):
        super().update(dt)
        self.button_group.update(dt)

    def draw(self, surface):
        super().draw(surface)

        if self.title_text:
            title_surf = self.title_font.render(self.title_text, True, self.title_color)
            title_rect = title_surf.get_rect(center=self.title_pos)
            surface.blit(title_surf, title_rect)

        self.button_group.draw(surface)