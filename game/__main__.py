from arcade import load_font

from .context import nav
from .menu import MenuView
from .window import Window


def main():
    # Load debug font
    load_font("resources/generic/gohu.ttf")

    win = Window(title="Game Dev Guild Jam 2026 Sem 2")
    nav.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
