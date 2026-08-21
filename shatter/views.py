from arcade import Camera2D, Sprite, SpriteList, View

from resources import get_spritesheet

from .navigation import navigation


class GameView(View):
    def __init__(self) -> None:
        super().__init__()
        self.camera = Camera2D(position=(0, 0))

        mirror_sheet = get_spritesheet("Mirror")
        mirror_frames = mirror_sheet.get_texture_grid((96, 96), 16, 32)
        self.mirror_body = tuple(mirror_frames[16:])
        self.mirror_shadow = tuple(mirror_frames[:16])

        self.mirror = Sprite(self.mirror_body[0], center_y=48)
        self.shadow = Sprite(self.mirror_shadow[0])

        self.player_layer = SpriteList()
        self.player_layer.extend((self.shadow, self.mirror))

    def on_draw(self) -> bool | None:
        self.clear(color=(125, 125, 125))
        with self.camera.activate():
            self.player_layer.draw(pixelated=True)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        from math import atan2, degrees

        wx, wy, _ = self.camera.unproject((x, y))
        self.mirror.position = (wx, wy + 48)
        self.shadow.position = (wx, wy)

        angle = degrees(atan2(self.shadow.center_y, self.shadow.center_x))
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
