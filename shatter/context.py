from dataclasses import dataclass
from enum import StrEnum
from arcade import get_window, SpriteList
from arcade.future.input import InputManager, Keys, ControllerAxes

from shatter.lib.navigation import NavigationStack

navigation = NavigationStack()

def setup_input_manager() -> InputManager:
    manager = InputManager()
    manager.new_axis("MoveHorizontal")
    manager.add_axis_input("MoveHorizontal", Keys.D, 1.0)
    manager.add_axis_input("MoveHorizontal", Keys.A, -1.0)
    manager.add_axis_input("MoveHorizontal", ControllerAxes.LEFT_STICK_X)
    manager.new_axis("MoveVertical")
    manager.add_axis_input("MoveVertical", Keys.W, 1.0)
    manager.add_axis_input("MoveVertical", Keys.S, -1.0)
    manager.add_axis_input("MoveVertical", ControllerAxes.LEFT_STICK_Y)

    manager.new_action("Pause")
    manager.add_action_input("Pause", Keys.ESCAPE)
    manager.new_action("Dash")
    manager.add_action_input("Dash", Keys.LSHIFT)
    manager.new_action("Catch")
    manager.add_action_input("Catch", Keys.SPACE)

    return manager

class Actions(StrEnum):
    Pause = "Pause"
    Dash = "Dash"
    Catch = "Catch"

class Axis(StrEnum):
    MoveHorizontal = "MoveHorizontal"
    MoveVertical = "MoveVertical"

def get_axis(name: Axis) -> float:
    return get_window().input.axis(name) # type: ignore

@dataclass
class GameLayers:
    ground: SpriteList
    shadows: SpriteList
    pieces: SpriteList