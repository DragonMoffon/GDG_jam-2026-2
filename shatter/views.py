from math import atan2, cos, degrees, pi, sin
from typing import Literal

from arcade import Sprite, View, draw_circle_filled, draw_line, key

from resources import get_spritesheet

from .collision import Circle, Line, collide
from .isometric import BillboardList, calculate_xy_intersection, create_isometric_camera
from .linear import Vec2
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
        self.mirror.depth = 48
        self.mirror_collider = Line(Vec2(self.shadow.center_x, self.shadow.center_y), Vec2(1.0, 0.0), 64.0)

        self.ball = Circle(Vec2(100.0, 0.0), 40.0)
        self.ball_velocity: Vec2 = Vec2(600.0, 0.0)

        self.billboards = BillboardList()
        self.billboards.extend((self.shadow, self.mirror))

        self.bounds: tuple[tuple[tuple[float, float], float]]

        self.alt = False

    def on_update(self, delta_time: float) -> bool | None:
        self.ball.center += (self.ball_velocity * delta_time)
        if collision := collide(self.mirror_collider, self.ball):
            along = collision.normal.dot(self.ball_velocity)

            if along < 0:
                self.ball.center += collision.normal * collision.depth
                self.ball_velocity -= collision.normal * (2 * along)

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            draw_line(0.0, 0.0, 100.0, 0.0, (255, 0, 0), 4)
            draw_line(0.0, 0.0, 0.0, 100.0, (0, 255, 0), 4)
            draw_circle_filled(
                self.ball.center.x, self.ball.center.y, self.ball.radius, (0, 0, 0, 125)
            )
            self.billboards.draw(pixelated=True)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        tx, ty = calculate_xy_intersection(self.camera, self.camera.unproject((x, y)))

        self.mirror.position = (tx, ty)
        self.shadow.position = (tx, ty)
        self.mirror_collider.center.update(tx, ty)

        if self.alt:
            return

        shadow_angle = atan2(ty, tx)
        self.mirror_collider.tangent.update(cos(shadow_angle - 0.5*pi), sin(shadow_angle - 0.5*pi))
        angle = degrees(shadow_angle) + 45
        frame = round(angle * 8 / 180)

        self.mirror.texture = self.mirror_body[frame]
        self.shadow.texture = self.mirror_shadow[frame]

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case key.LSHIFT:
                self.alt = True

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case key.LSHIFT:
                self.alt = False


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
