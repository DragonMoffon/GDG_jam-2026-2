from arcade import SpriteList, View, Rect
from arcade.camera import OrthographicProjector

from shatter.isometric import create_isometric_camera, calculate_xy_intersection, BillboardList
from shatter.linear import Vec2
from shatter.collision import World, Plane, CollisionLayers
from shatter.pieces.orb import Orb


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
        self.ground: SpriteList = SpriteList()
        self.billboard: BillboardList = BillboardList()

        self.camera = create_isometric_camera((0.0, 0.0), self.height, self.window.rect)

        self.orb = Orb(Vec2(0.0, 0.0))
        self.orb.attach(self.world, self.billboard, self.ground)

        for wall in get_walls(self.window.rect, self.camera):
            self.world.add_collider(wall)

    def on_update(self, delta_time: float) -> bool | None:
        self.orb.update(delta_time)
        self.world.update()

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            with self.window.ctx.enabled(self.window.ctx.DEPTH_TEST):
                self.ground.draw(pixelated=True)
                self.orb.draw()
                self.billboard.draw(pixelated=True)