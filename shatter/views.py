from arcade import Sprite, View, draw_circle_filled, draw_line

from resources import get_spritesheet

from .isometric import BillboardList, calculate_xy_intersection, create_isometric_camera
from .navigation import navigation


class GameView(View):
    def __init__(self) -> None:
        super().__init__()
        self.camera = create_isometric_camera((0.0, 0.0), self.height, self.window.rect)

        mirror_sheet = get_spritesheet("Mirror")
        mirror_frames = mirror_sheet.get_texture_grid((96, 96), 16, 32)
        self.mirror_body = tuple(mirror_frames[16:])
        self.mirror_shadow = tuple(mirror_frames[:16])

        self.mirror = Sprite(self.mirror_body[0], center_y=48)
        self.shadow = Sprite(self.mirror_shadow[0])

        self.player_layer = BillboardList()
        self.player_layer.extend((self.shadow, self.mirror))

        self.ball_position = (0.0, 0.0)
        self.ball_velocity = (100.0, 0.0)

    def on_update(self, delta_time: float) -> bool | None:
        self.ball_position = (
            self.ball_position[0] + delta_time * self.ball_velocity[0],
            self.ball_position[1] + delta_time * self.ball_velocity[1],
        )

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            draw_line(0.0, 0.0, 100.0, 0.0, (255, 0, 0), 4)
            draw_line(0.0, 0.0, 0.0, 100.0, (0, 255, 0), 4)
            draw_circle_filled(self.ball_position[0], self.ball_position[1], 20, (0, 0, 0))
            self.player_layer.draw(pixelated=True)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        from math import atan2, degrees

        tx, ty = calculate_xy_intersection(self.camera, self.camera.unproject((x, y)))

        self.mirror.position = (tx, ty)
        self.mirror.depth = 48
        self.shadow.position = (tx, ty)
        self.shadow.depth = 0

        angle = degrees(atan2(ty, tx)) + 45
        frame = round(angle * 8 / 180)

        self.mirror.texture = self.mirror_body[frame]
        self.shadow.texture = self.mirror_shadow[frame]


class MenuView(View):
    def on_draw(self) -> bool | None:
        from arcade import draw_text

        self.clear()
        draw_text(
            "Main Menu\nPress Anything To Start",
            self.center_x,
            self.center_y,
            multiline=True,
            width=int(self.width),
            align="center",
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if navigation.peek() is self:
            navigation.push(GameView())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if navigation.peek() is self:
            navigation.push(GameView())
