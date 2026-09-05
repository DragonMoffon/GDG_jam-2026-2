from arcade import SpriteList, View, Rect, draw_point
from arcade.camera import OrthographicProjector
from arcade.future.input import ActionState

from shatter.isometric import create_isometric_camera, calculate_xy_intersection, BillboardList
from shatter.context import navigation
from shatter.linear import Vec2
from shatter.collision import World, Plane, CollisionLayers
from shatter.context import Actions, GameLayers
from shatter.pieces.orb import Orb
from shatter.pieces.player import Player


def get_walls(rect: Rect, camera: OrthographicProjector):
    bl = Vec2(calculate_xy_intersection(camera, camera.unproject(rect.bottom_left)))
    tl = Vec2(calculate_xy_intersection(camera, camera.unproject(rect.top_left)))
    tr = Vec2(calculate_xy_intersection(camera, camera.unproject(rect.top_right)))
    br = Vec2(calculate_xy_intersection(camera, camera.unproject(rect.bottom_right)))

    yield Plane(CollisionLayers.GEOMETRY, CollisionLayers.NONE, -(bl + tl).normalised(), -0.5 * (bl+tl).length)
    yield Plane(CollisionLayers.GEOMETRY, CollisionLayers.NONE, -(tl + tr).normalised(), -0.5 * (tl+tr).length)
    yield Plane(CollisionLayers.GEOMETRY, CollisionLayers.NONE, -(tr + br).normalised(), -0.5 * (tr+br).length)
    yield Plane(CollisionLayers.GEOMETRY, CollisionLayers.NONE, -(br + bl).normalised(), -0.5 * (br+bl).length)

class GameView(View):

    def __init__(self) -> None:
        super().__init__()
        self.world = World()
        self.render_layers = GameLayers(
            SpriteList(),
            BillboardList(),
            BillboardList()
        )

        self.camera = create_isometric_camera((0.0, 0.0), self.height, self.window.rect)

        self.player = Player()
        self.player.attach(self.world, self.render_layers)

        self.orb = Orb(Vec2(0.0, 0.0))
        self.orb.attach(self.world, self.render_layers)

        for wall in get_walls(self.window.rect, self.camera):
            self.world.add_collider(wall)

        print(self.player.mirror.collider.layer & self.orb.collider.mask)

    def on_update(self, delta_time: float) -> bool | None:
        self.player.update(delta_time)
        self.orb.update(delta_time)
        self.world.update()

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            self.render_layers.ground.draw(pixelated=True)
            self.render_layers.shadows.draw(pixelated=True)
            with self.window.ctx.enabled(self.window.ctx.DEPTH_TEST):
                self.render_layers.pieces.draw(pixelated=True)
            draw_point(self.player.mirror.collider.center.x, self.player.mirror.collider.center.y, (255, 0, 0), 10)

    def on_action(self, action: str, pressed: ActionState):
        if pressed == ActionState.PRESSED and action == Actions.Pause:
            navigation.pop()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        tx, ty = calculate_xy_intersection(self.camera, self.camera.unproject((x, y)))
        self.player.on_mouse_motion(tx, ty)