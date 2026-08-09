from .window import Window
from .chessehc import ChessehcView
from arcade import load_font


def main():
    # Load debug font
    load_font("resources/generic/gohu.ttf")

    win = Window(title="Game Dev Guild Jam 2026 Sem 2")
    win.run(ChessehcView())


if __name__ == "__main__":
    main()
