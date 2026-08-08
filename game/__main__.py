from .window import Window
from .chessehc import ChessehcView


def main():
    win = Window(title="Game Dev Guild Jam 2026 Sem 2")
    win.run(ChessehcView())


if __name__ == "__main__":
    main()
