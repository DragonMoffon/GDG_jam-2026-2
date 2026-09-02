from math import cos, pi, radians, sin

from arcade import Rect, SpriteList
from arcade.camera import CameraData, OrthographicProjectionData, OrthographicProjector
from arcade.texture_atlas import TextureAtlasBase
from arcade.types import Point2, Point3

from resources import get_shader_path

# Isometric position x, y with z up on screen
_THETA = radians(225.0)
_PHI = radians(26.5)
_TX, _TY = cos(_THETA), sin(_THETA)
_PXY, _PZ = cos(_PHI), sin(_PHI)
_UXY, _UZ = cos(_PHI - 0.5 * pi), sin(_PHI - 0.5 * pi)

def create_isometric_camera(focus: Point2, distance: float, viewport: Rect):
    view = CameraData(
        (focus[0] + distance * _TX * _PXY, focus[1] + distance * _TY * _PXY, distance * _PZ),
        (-_TX * _UXY, -_TY * _UXY, -_UZ),
        (-_TX * _PXY, -_TY * _PXY, -_PZ),
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

def focus_isometric(focus: Point2, distance: float, camera: CameraData):
    camera.position = (focus[0] + distance * _TX * _PXY, focus[1] + distance * _TY * _PXY, distance * _PZ)


def calculate_xy_intersection(projection: OrthographicProjector, position: Point3) -> tuple[float, float]:
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

        program = self.ctx.load_program(
            vertex_shader=":system:shaders/sprites/sprite_list_geometry_vs.glsl",
            geometry_shader=get_shader_path("sprite_list_billboard_cull_geo"),
            fragment_shader=":system:shaders/sprites/sprite_list_geometry_fs.glsl",
        )
        program["sprite_texture"] = 0
        program["uv_texture"] = 1

        self.data.program = program # type: ignore
