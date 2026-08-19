from sys import exit
from graphics.screen import Button_Screen
from graphics.image_handler import Image_Handler
from graphics.ui import Button

class Main_Screen(Button_Screen):

    def __init__(self, image_handler: Image_Handler,
                 background_path="./assets/images/screen_backgrounds/main_screen.jpg"):
        button_specs = [
            ("Play", None),      
            ("Options", None),  
            ("Credits", lambda: image_handler.set_scene("credits")),
            ("Quit", lambda: exit()), 
        ]
        super().__init__(
            name="main_screen",
            image_handler=image_handler,
            background_path=background_path,
            title_text="Kellox Basement",
            button_specs=button_specs,
        )
        # button = Button("",(200,0),visible=False)
        # drawable = image_handler.load_drawable("./assets/images/horn.jpg","horn")
        # button.set_callback(lambda: image_handler.add_drawable_to_current_scene(drawable))
        # self.button_group.add(button)