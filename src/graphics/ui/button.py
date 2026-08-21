import pygame
from typing import Callable


class Button:

    def __init__(self, text: str, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (240, 60),
                 on_click: Callable[[], None] | None = None, font: pygame.font.Font | None = None,
                 bg_color: tuple[int, int, int] = (70, 70, 90), hover_color: tuple[int, int, int] = (100, 100, 130),
                 disabled_color: tuple[int, int, int] = (45, 45, 55), text_color: tuple[int, int, int] = (255, 255, 255),
                 enabled: bool = True, visible: bool = True) -> None:
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.on_click = on_click
        self.font = font or pygame.font.SysFont(None, 32)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.text_color = text_color
        self.hovered = False
        self.enabled = enabled
        self.visible = visible

    def set_callback(self, callback: Callable[[], None]) -> None:
        """
        Executes function on click
        For Example:
        button.set_callback(lambda: game.change_mode('playing'))
        """
        self.on_click = callback

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.rect.topleft = pos

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled or not self.visible:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()
                else:
                    print(f"Button '{self.text}' clicked (no callback set yet)")

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return

        if not self.enabled:
            color = self.disabled_color
        else:
            color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (20, 20, 20), self.rect, width=2, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class ButtonGroup:
    """
    Owns a list of Buttons and takes care of layout, event forwarding and
    drawing as one unit, so a screen just needs one ButtonGroup instead of
    hand-rolling a for-loop for events/draw and its own layout math.
    """

    def __init__(self, buttons: list[Button] | None = None) -> None:
        self.buttons = list(buttons) if buttons else []

    def add(self, button: Button) -> Button:
        self.buttons.append(button)
        return button

    def get(self, label: str) -> Button | None:
        """Look up a button by its text."""
        for button in self.buttons:
            if button.text == label:
                return button
        return None

    def layout_vertical(self, center_x: int, start_y: int, spacing: int = 20) -> None:
        """Stack all buttons vertically, each centered on center_x."""
        y = start_y
        for button in self.buttons:
            button.rect.centerx = center_x
            button.rect.top = y
            y += button.rect.height + spacing

    def layout_vertical_centered(self, screen_size: tuple[int, int], spacing: int = 20) -> None:
        """Stack all buttons vertically and center the whole stack
        within screen_size."""
        if not self.buttons:
            return
        screen_w, screen_h = screen_size
        total_height = (sum(b.rect.height for b in self.buttons)
                         + spacing * (len(self.buttons) - 1))
        start_y = (screen_h - total_height) // 2
        self.layout_vertical(screen_w // 2, start_y, spacing)

    def layout_horizontal(self, center_y: int, start_x: int, spacing: int = 20) -> None:
        """Line all buttons up horizontally, each centered on center_y."""
        x = start_x
        for button in self.buttons:
            button.rect.centery = center_y
            button.rect.left = x
            x += button.rect.width + spacing

    def handle_event(self, event: pygame.event.Event) -> None:
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float) -> None:
        pass  # placeholder in case buttons ever need per-frame logic

    def draw(self, surface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(surface)