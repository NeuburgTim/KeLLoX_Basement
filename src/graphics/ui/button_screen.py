"""
Generic base class for "background + title + a stack of buttons" screens
like the main menu or the credits screen.
"""

import pygame
from graphics.scene import Scene
from graphics.ui.button import Button, ButtonGroup


class ButtonScreen(Scene):

    def __init__(self, name: str, app: "GameApp", background_path: str | None = None,
                 title_text: str | None = None, title_font: pygame.font.Font | None = None,
                 title_color: tuple[int, int, int] = (255, 255, 255),
                 title_pos: tuple[int, int] | None = None, button_specs: list | tuple = (),
                 button_size: tuple[int, int] = (240, 60),
                 button_font: pygame.font.Font | None = None, button_spacing: int = 20) -> None:
        """
        name:            scene name, used by SceneManager.set_scene()
        app:             the GameApp instance â€” gives access to .assets,
                         .screen, .game_data and .change_mode()
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
            background = app.assets.load_image(background_path, scale=app.screen.get_size())
        super().__init__(name=name, background=background)

        self.app = app

        self.title_text = title_text
        self.title_font = title_font or (pygame.font.SysFont(None, 64) if title_text else None)
        self.title_color = title_color
        screen_w, _ = app.screen.get_size()
        self.title_pos = title_pos or (screen_w // 2, 100)

        self.button_group = ButtonGroup()
        self._build_buttons(button_specs, button_size, button_font, button_spacing)

    def _build_buttons(self, button_specs: list | tuple, button_size: tuple[int, int],
                        button_font: pygame.font.Font | None, spacing: int) -> None:
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
            self.app.screen.get_size(), spacing=spacing
        )

    def get_button(self, label: str) -> Button | None:
        """Look up a button by its text, e.g.:
        screen.get_button("Play").set_callback(...)
        """
        return self.button_group.get(label)

    def handle_event(self, event: pygame.event.Event) -> None:
        """GameApp forwards raw pygame events here."""
        self.button_group.handle_event(event)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.button_group.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)

        if self.title_text:
            title_surf = self.title_font.render(self.title_text, True, self.title_color)
            title_rect = title_surf.get_rect(center=self.title_pos)
            surface.blit(title_surf, title_rect)

        self.button_group.draw(surface)