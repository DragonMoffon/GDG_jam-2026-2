from math import atan2, cos, degrees, pi, sin
from typing import Literal

from arcade import Sprite, View, draw_circle_filled, draw_line, key

from resources import get_spritesheet

from .isometric import BillboardList, calculate_xy_intersection, create_isometric_camera
from .navigation import navigation


def draw_linebox(o: tuple[float, float], a: float, d: float):
    c = 0.5 * d * cos(a)
    s = 0.5 * d * sin(a)
    x1, x2 = o[0] - c, o[0] + c
    y1, y2 = o[1] - s, o[1] + s

    draw_line(x1, y1, x2, y2, (255, 0, 0), 4)
    draw_line(o[0], o[1], o[0] - s, o[1] + c, (0, 255, 0), 2)


def line_sphere_collision(
    origin: tuple[float, float],
    direction: tuple[float, float],
    width: float,
    center: tuple[float, float],
    radius: float,
) -> Literal[False] | tuple[tuple[float, float], float]:
    # https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection 2025-08-27
    diff = origin[0] - center[0], origin[1] - center[1]
    length = (diff[0] ** 2 + diff[1] ** 2) ** 0.5
    across = direction[0] * diff[0] + direction[1] * diff[1]
    nabla = across**2 - length**2 + radius**2

    if nabla < 0:  # Line never intersects circle
        return False

    sqrt_nabla = nabla**0.5
    h_width = 0.5 * width
    d1 = -direction[0] * diff[0] - direction[1] * diff[1] + sqrt_nabla
    d2 = -direction[0] * diff[0] - direction[1] * diff[1] - sqrt_nabla

    if (
        h_width < abs(d1) and h_width < abs(d2) and radius < length
    ):  # Line segment never intersects circle and is outside of it
        return False

    normal = -direction[1], direction[0]
    # Normal is from line to sphere, but diff is sphere to line so we need to flip it
    separation = -(normal[0] * diff[0] + normal[1] * diff[1])
    abs_separation = abs(separation)
    sign = separation / abs_separation

    # Direction to surface of sphere and depth into sphere
    return (normal[0] * sign, normal[1] * sign), radius - abs_separation


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

        self.shadow_angle: float = 0.0
        self.shadow_width: float = 64.0

        self.ball_position = (10, 0.0)
        self.ball_velocity = (600.0, 0.0)
        self.ball_radius = 40

        self.billboards = BillboardList()
        self.billboards.extend((self.shadow, self.mirror))

        self.bounds: tuple[tuple[tuple[float, float], float]]

        self.alt = False

    def on_update(self, delta_time: float) -> bool | None:
        self.ball_position = (
            self.ball_position[0] + delta_time * self.ball_velocity[0],
            self.ball_position[1] + delta_time * self.ball_velocity[1],
        )

        if collision := line_sphere_collision(
            self.shadow.position,
            (cos(self.shadow_angle - 0.5 * pi), sin(self.shadow_angle - 0.5 * pi)),
            self.shadow_width,
            self.ball_position,
            self.ball_radius,
        ):
            print("collision ->", collision)
            normal, depth = collision
            along = normal[0] * self.ball_velocity[0] + normal[1] * self.ball_velocity[1]
            if along < 0:
                self.ball_position = (
                    self.ball_position[0] + normal[0] * depth,
                    self.ball_position[1] + normal[1] * depth,
                )
                self.ball_velocity = (
                    self.ball_velocity[0] - 2 * along * normal[0],
                    self.ball_velocity[1] - 2 * along * normal[1],
                )

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            draw_line(0.0, 0.0, 100.0, 0.0, (255, 0, 0), 4)
            draw_line(0.0, 0.0, 0.0, 100.0, (0, 255, 0), 4)
            draw_circle_filled(
                self.ball_position[0], self.ball_position[1], self.ball_radius, (0, 0, 0, 125)
            )
            draw_line(
                self.ball_position[0],
                self.ball_position[1],
                self.ball_position[0] + self.ball_velocity[0],
                self.ball_position[1] + self.ball_velocity[1],
                (255, 255, 255),
                2,
            )
            draw_linebox(self.shadow.position, self.shadow_angle - 0.5 * pi, self.shadow_width)
            self.billboards.draw(pixelated=True)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        tx, ty = calculate_xy_intersection(self.camera, self.camera.unproject((x, y)))

        self.mirror.position = (tx, ty)
        self.mirror.depth = 48
        self.shadow.position = (tx, ty)
        self.shadow.depth = 0

        if self.alt:
            return

        self.shadow_angle = atan2(ty, tx)
        angle = degrees(self.shadow_angle) + 45
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
