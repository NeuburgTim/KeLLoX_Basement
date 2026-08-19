import pygame
from sys import exit
from graphics.image_handler import Scene
from graphics.image_handler import Image_Handler

class Button:

    def __init__(self, text, pos, size=(240, 60), on_click=None, font=None,
                 bg_color=(70, 70, 90), hover_color=(100, 100, 130),
                 text_color=(255, 255, 255)):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.on_click = on_click
        self.font = font or pygame.font.SysFont(None, 32)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.enabled = True

    def set_callback(self, callback):
        """
        Executes function on click
        For Example:
        button.set_callback(lambda: game.change_state('playing'))
        """
        self.on_click = callback

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()
                else:
                    print(f"Button '{self.text}' clicked (no callback set yet)")

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (20, 20, 20), self.rect, width=2, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Main_Screen(Scene):

    def __init__(self, image_handler:Image_Handler, 
                 background_path="./assets/images/screen_backgrounds/main_screen.jpg",
                 button_labels=("Play", "Options", "Credits", "Quit")):
        background = None
        if background_path:
            background = image_handler.load_image(
                background_path, scale=image_handler.screen.get_size()
            )
        super().__init__(name="main_screen", background=background)

        self.image_handler = image_handler
        self.title_font = pygame.font.SysFont(None, 64)
        self.title_text = "Kellox Basement"

        self.buttons = []
        self._build_buttons(button_labels)

    def _build_buttons(self, labels):
        screen_w, screen_h = self.image_handler.screen.get_size()
        button_width, button_height = 240, 60
        spacing = 20

        total_height = len(labels) * button_height + (len(labels) - 1) * spacing
        start_y = (screen_h - total_height) // 2
        x = (screen_w - button_width) // 2

        for i, label in enumerate(labels):
            y = start_y + i * (button_height + spacing)
            new_button = Button(label, (x, y), (button_width, button_height))
            self.buttons.append(new_button)
            if label == "Quit":
                new_button.set_callback(lambda: exit()) #nochmal ueberarbeiten
            if label == "Credits":
                new_button.set_callback(lambda: self.image_handler.set_scene("credits"))
                

        # button = Button("Beispiel",(0,200),(240,60))
        # drawable = self.image_handler.load_drawable("./assets/images/horn.jpg","test")
        # button.set_callback(lambda:self.image_handler.add_drawable_to_scene("main_screen",drawable))
        # self.buttons.append(button)

    def get_button(self, label):
        """
        Look up button by text
        """
        for button in self.buttons:
            if button.text == label:
                return button
        return None

    
    def handle_event(self, event):
        """Image_Handler/Game_State should forward raw pygame events here"""
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        super().draw(surface)

        title_surf = self.title_font.render(self.title_text, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(surface.get_width() // 2, 100))
        surface.blit(title_surf, title_rect)

        for button in self.buttons:
            button.draw(surface)