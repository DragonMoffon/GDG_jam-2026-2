from arcade import Window as ArcadeWindow
from arcade.future.input import InputManager


class Window(ArcadeWindow):
    def __init__(self):
        super().__init__(1280, 720, "Shatter -- GDG Jam 2026-2 --")
        self.input: InputManager = InputManager()
