from pathlib import Path

from arcade import SpriteSheet, Texture, load_font, load_spritesheet, load_texture

root = Path() / "resources"

textures: dict[str, Path] = {
    pth.stem: pth for pth in (root / "textures").iterdir() if pth.suffix == ".png" and pth.is_file()
}

fonts: tuple[Path, ...] = tuple(
    pth
    for pth in (root / "fonts").iterdir()
    if (pth.suffix == ".ttf" or pth.suffix == ".otf") and pth.is_file()
)

shaders: dict[str, Path] = {
    pth.stem: pth for pth in (root / "shaders").iterdir() if pth.suffix == ".glsl" and pth.is_file()
}


def setup():
    for font in fonts:
        load_font(font)


def get_texture(name: str) -> Texture:
    return load_texture(textures[name])


def get_spritesheet(name: str) -> SpriteSheet:
    return load_spritesheet(textures[name])


def get_shader_path(name: str) -> Path:
    return shaders[name]
