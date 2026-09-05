from math import cos, pi, sin, sqrt
from random import uniform

from arcade import XYWH, Camera2D, Sprite, View, draw_circle_filled, draw_sprite, key
from arcade.clock import GLOBAL_FIXED_CLOCK
from arcade.math import lerp, lerp_2d
from arcade.types import Point2

from .context import nav

PLAYER_SPEED = 45
MAX_SPEED = 500

RADIUS_RANGE = (1.0, 32.0)

ACCELERATION = 10.0
WIDTH = 256
H_WIDTH = 0.5 * WIDTH
HEIGHT = 144
H_HEIGHT = 0.5 * HEIGHT


def accelerate(acc: float, vel: float) -> float:
    return acc * sqrt(1 - (vel / MAX_SPEED) ** 2) if vel < MAX_SPEED else 0.0


class Projectile:
    def __init__(self) -> None:
        r = uniform(-pi, pi)
        c, s = cos(r), sin(r)
        self._p_rad: float
        self._p_loc: tuple[float, float]
        self._p_vel: tuple[float, float]
        self._radius: float = RADIUS_RANGE[0]
        self._location: tuple[float, float] = (0.0, 0.0)
        self._velocity: tuple[float, float] = (1 * c, 1 * s)

        self.tick(0.0)

    def tick(self, dt: float):
        self._p_rad = self._radius
        self._p_loc = self._location
        self._p_vel = self._velocity
        sx, sy = self._location
        dx, dy = self._velocity

        x = sx + dt * dx
        y = sy + dt * dy
        speed = (dx**2 + dy**2) ** 0.5
        self._radius = radius = lerp(RADIUS_RANGE[0], RADIUS_RANGE[1], speed / MAX_SPEED)

        if x < radius - H_WIDTH:
            x = radius - H_WIDTH
            dx = abs(dx)
        elif H_WIDTH - radius < x:
            x = H_WIDTH - radius
            dx = -abs(dx)

        if y < radius - H_HEIGHT:
            y = radius - H_HEIGHT
            dy = abs(dy)
        elif H_HEIGHT - radius < y:
            y = H_HEIGHT - radius
            dy = -abs(dy)

        self._location = x, y
        self._velocity = dx, dy

    def draw(self):
        t = GLOBAL_FIXED_CLOCK.fraction

        x, y = lerp_2d(self._p_loc, self._location, t)
        r = lerp(self._p_rad, self._radius, t)
        draw_circle_filled(x, y, r, (255, 255, 255), num_segments=16)


class ReboundView(View):
    def __init__(self) -> None:
        super().__init__()

        self.camera = Camera2D(projection=XYWH(0, 0, WIDTH, HEIGHT), position=(0.0, 0.0))

        self.player = Sprite("resources/rebound/knight.png")
        self.sphere = Projectile()
        self.impulse: Point2 | None = None

        self.vertical: int = 0
        self.horizontal: int = 0

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case key.W:
                self.vertical = min(1, self.vertical + 1)
            case key.S:
                self.vertical = max(-1, self.vertical - 1)
            case key.D:
                self.horizontal = min(1, self.horizontal + 1)
            case key.A:
                self.horizontal = max(-1, self.horizontal - 1)
            case key.SPACE:
                self.impulse = self.player.position
            case key.BACKSPACE:
                nav.pop()

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case key.W:
                self.vertical = max(-1, self.vertical - 1)
            case key.S:
                self.vertical = min(1, self.vertical + 1)
            case key.D:
                self.horizontal = max(-1, self.horizontal - 1)
            case key.A:
                self.horizontal = min(1, self.horizontal + 1)

    def on_fixed_update(self, delta_time: float):

        dx = self.horizontal * PLAYER_SPEED * delta_time
        dy = self.vertical * PLAYER_SPEED * delta_time

        if dx or dy:
            speed = (dx**2 + dy**2) ** 0.5
            dx = dx / speed
            dy = dy / speed

        self.player.position = self.player.center_x + dx, self.player.center_y + dy
        if self.impulse is not None:
            dist_x = self.sphere._location[0] - self.impulse[0]
            dist_y = self.sphere._location[1] - self.impulse[1]
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if self.sphere._radius < dist:
                nx = dist_x / dist
                ny = dist_y / dist
                tx = -ny
                ty = nx
                vx, vy = self.sphere._velocity
                v = (vx**2 + vy**2) ** 0.5

                nv = nx * vx + ny * vy
                if nv <= 0:
                    new_v = min(v + accelerate(ACCELERATION, v), MAX_SPEED)
                    self.sphere._velocity = nx * new_v, ny * new_v
            self.impulse = None
        self.sphere.tick(delta_time)

    def on_draw(self) -> bool | None:
        self.clear()
        with self.camera.activate():
            draw_sprite(self.player, pixelated=True)
            self.sphere.draw()
