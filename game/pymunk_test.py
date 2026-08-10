"""
To learn Pymunk I wanna try take a pymunk example (which uses pygame blegh) to use arcade
"""

import random
from enum import IntEnum

import arcade
import pymunk


class CollisionType(IntEnum):
    ball = 1
    brick = 2
    bottom = 3
    player = 4


def spawn_ball(space: pymunk.Space, position: pymunk.Vec2d, direction: pymunk.Vec2d):
    body = pymunk.Body(1, float("inf"))
    body.position = position

    shape = pymunk.Circle(body, 5)
    shape.elasticity = 1.0
    shape.collision_type = CollisionType.ball

    body.apply_impulse_at_local_point(direction)

    def constant_velocity(body: pymunk.Body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400.0

    body.velocity_func = constant_velocity

    space.add(body, shape)


def setup_level(
    space: pymunk.Space, player: pymunk.Body, start: tuple[float, float], size: tuple[float, float]
):
    for s in list(space.shapes):
        if s.body.body_type == pymunk.Body.DYNAMIC and s.body is not player:
            space.remove(s.body, s)

    spawn_ball(space, player.position + (0, 40), pymunk.Vec2d(random.choice((1, -1)), 10))

    for x in range(21):
        x = x * size[0] + start[0]
        for y in range(5):
            y = y * size[1] + start[1]
            brick = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            brick.position = x, y
            brick_shape = pymunk.Poly.create_box(brick, size)
            brick_shape.elasticity = 1.0
            brick_shape.collision_type = CollisionType.brick
            space.add(brick, brick_shape)

    def remove_brick(arbiter, space, data):
        brick_shape = arbiter.shapes[0]
        space.remove(brick_shape, brick_shape.body)

    space.add_collision_handler(CollisionType.brick, CollisionType.ball).separate = remove_brick


class BreakoutView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.space = pymunk.Space()
        static_lines = (
            pymunk.Segment(self.space.static_body, (50, 50), (50, self.height - 50), 2),
            pymunk.Segment(
                self.space.static_body,
                (50, self.height - 50),
                (self.width - 50, self.height - 50),
                2,
            ),
            pymunk.Segment(
                self.space.static_body,
                (self.width - 50, self.height - 50),
                (self.width - 50, 50),
                2,
            ),
        )
        for line in static_lines:
            line.elasticity = 1.0
        self.space.add(*static_lines)

        bottom = pymunk.Segment(self.space.static_body, (50, 50), (self.width - 50, 50), 2)
        bottom.sensor = True
        bottom.collision_type = CollisionType.bottom

        def remove_first(arbiter, space, data):
            ball = arbiter.shapes[0]
            space.remove(ball, ball.body)
            return False

        self.space.add_collision_handler(
            CollisionType.ball, CollisionType.bottom
        ).begin = remove_first
        self.space.add(bottom)

        self.player = pymunk.Body(500, float("inf"))
        self.player.position = 0.5 * self.width, 100

        player_shape = pymunk.Segment(self.player, (-50, 0), (50, 0), 8)
        player_shape.elasticity = 1.0
        player_shape.collision_type = CollisionType.player

        def pre_solve(arbiter, space, data):
            set_ = arbiter.contact_point_set
            if len(set_.points) > 0:
                player = arbiter.shapes[0]
                delta = (player.body.position - set_.points[0].point_a).x
                normal = pymunk.Vec2d(0, 1).rotated(delta / 50.0)
                set_.normal = normal
                set_.points[0].distance = 0
            arbiter.contact_point_set = set_
            return True

        self.space.add_collision_handler(
            CollisionType.player, CollisionType.ball
        ).pre_solve = pre_solve

        joint = pymunk.GrooveJoint(
            self.space.static_body, self.player, (100, 100), (self.width - 100, 100), (0, 0)
        )
        self.space.add(self.player, player_shape, joint)

        setup_level(
            self.space, self.player, (100, self.height - 150), ((self.width - 200) / 20, 20)
        )

        self.movement: int = 0

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case arcade.key.A:
                self.movement = max(-1, self.movement - 1)
            case arcade.key.D:
                self.movement = min(1, self.movement + 1)
            case arcade.key.R:
                setup_level(
                    self.space, self.player, (100, self.height - 150), ((self.width - 200) / 20, 20)
                )
            case arcade.key.SPACE:
                spawn_ball(
                    self.space,
                    self.player.position + (0, 40),
                    pymunk.Vec2d(random.choice((1, -1)), 10),
                )

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case arcade.key.A:
                self.movement = min(1, self.movement + 1)
            case arcade.key.D:
                self.movement = max(-1, self.movement - 1)

    def on_draw(self):
        self.clear()
        for shape in self.space.shapes:
            if shape.sensor:
                continue
            body = shape.body
            match shape:
                case pymunk.Circle():
                    arcade.draw_circle_filled(
                        body.position.x, body.position.y, shape.radius, (255, 0, 0)
                    )
                case pymunk.Segment():
                    arcade.draw_line(
                        body.position.x + shape.a[0],
                        body.position.y + shape.a[1],
                        body.position.x + shape.b[0],
                        body.position.y + shape.b[1],
                        (125, 125, 125),
                        shape.radius,
                    )
                case pymunk.Poly():
                    verts = shape.get_vertices()
                    verts = (*verts, verts[0])
                    arcade.draw_line_strip(
                        tuple(point + body.position for point in verts),
                        (255, 0, 0),
                        2,
                    )

    def on_fixed_update(self, delta_time: float):
        self.player.velocity = (600 * self.movement, 0)
        self.space.step(delta_time)
