from arcade import Window as ArcadeWindow
from arcade.future.input import InputManager, Keys, ControllerAxes

from .context import setup_input_manager


class Window(ArcadeWindow):
    def __init__(self):
        super().__init__(1280, 720, "Shatter -- GDG Jam 2026-2 --")
        self.input: InputManager = setup_input_manager()

    def on_update(self, delta_time: float) -> bool | None:
        self.input.update()