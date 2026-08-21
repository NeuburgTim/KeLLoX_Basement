import sys
from graphics.ui.button_screen import ButtonScreen


class MainMenuScreen(ButtonScreen):

    def __init__(self, app: "GameApp", background_path: str = "./assets/images/screen_backgrounds/main_screen.jpg") -> None:
        button_specs = [
            ("Play", None),
            ("Options", None),
            ("Credits", lambda: app.change_mode("credits")),
            ("Quit", lambda: sys.exit()),
        ]
        super().__init__(
            name="main_menu",
            app=app,
            background_path=background_path,
            title_text="Kellox Basement",
            button_specs=button_specs,
        )