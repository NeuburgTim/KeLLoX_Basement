from graphics.screen import Button_Screen
from graphics.image_handler import Image_Handler


class Credits_Screen(Button_Screen):
    def __init__(self, image_handler: Image_Handler, background_path="./assets/images/screen_backgrounds/credit_screen.png"):
        button_specs = [
            ("Back", lambda: image_handler.set_scene("main_screen")),
        ]
        super().__init__(
            name="credits",
            image_handler=image_handler,
            background_path=background_path,
            title_text="Credits",
            button_specs=button_specs,
        )