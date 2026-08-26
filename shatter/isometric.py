from math import cos, pi, radians, sin

from arcade import Rect, SpriteList
from arcade.camera import CameraData, OrthographicProjectionData, OrthographicProjector
from arcade.texture_atlas import TextureAtlasBase
from arcade.types import Point2, Point3

from resources import get_shader_path


def create_isometric_camera(focus: Point2, distance: float, viewport: Rect):
    theta, phi = radians(225), radians(26.5)  # Isometric position with x, y up on screen
    tx, ty = cos(theta), sin(theta)
    pxy, pz = cos(phi), sin(phi)
    uxy, uz = cos(phi - 0.5 * pi), sin(phi - 0.5 * pi)

    view = CameraData(
        (focus[0] + distance * tx * pxy, focus[1] + distance * ty * pxy, distance * pz),
        (-tx * uxy, -ty * uxy, -uz),
        (-tx * pxy, -ty * pxy, -pz),
    )
    proj = OrthographicProjectionData(
        -0.5 * viewport.width,
        0.5 * viewport.width,
        -0.5 * viewport.height,
        0.5 * viewport.height,
        -100.0,
        2.0 * distance + 100.0,
    )

    return OrthographicProjector(view=view, projection=proj, viewport=viewport)


def calculate_xy_intersection(projection: OrthographicProjector, position: Point3) -> Point2:
    # For an orthographic projection the depth is the z-position divided by the forward vector
    depth = -position[2] / projection.view.forward[2]
    x = position[0] + depth * projection.view.forward[0]
    y = position[1] + depth * projection.view.forward[1]
    return x, y


class BillboardList(SpriteList):
    def __init__(
        self,
        use_spatial_hash: bool = False,
        spatial_hash_cell_size: int = 128,
        atlas: TextureAtlasBase | None = None,
        capacity: int = 100,
        lazy: bool = False,
        visible: bool = True,
    ) -> None:
        super().__init__(use_spatial_hash, spatial_hash_cell_size, atlas, capacity, lazy, visible)

        self.data.program = self.ctx.load_program(
            vertex_shader=":system:shaders/sprites/sprite_list_geometry_vs.glsl",
            geometry_shader=get_shader_path("sprite_list_billboard_cull_geo"),
            fragment_shader=":system:shaders/sprites/sprite_list_geometry_fs.glsl",
        )
        self.data.program["sprite_texture"] = 0
        self.data.program["uv_texture"] = 1
