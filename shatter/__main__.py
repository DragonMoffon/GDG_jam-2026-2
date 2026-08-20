from arcade import load_font

from .navigation import navigation
from .window import Window


def main():
    # Load debug font
    load_font("resources/generic/gohu.ttf")

    win = Window(title="Game Dev Guild Jam 2026 Sem 2")
    # navigation.setup(,win)
    win.run()


if __name__ == "__main__":
    main()
