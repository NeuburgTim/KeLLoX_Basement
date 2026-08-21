from graphics.ui.button_screen import ButtonScreen


class CreditsScreen(ButtonScreen):

    def __init__(self, app, background_path="./assets/images/screen_backgrounds/credit_screen.png"):
        button_specs = [
            ("Back", lambda: app.change_mode("main_menu")),
        ]
        super().__init__(
            name="credits",
            app=app,
            background_path=background_path,
            title_text="Credits",
            button_specs=button_specs,
        )
