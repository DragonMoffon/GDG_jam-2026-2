from arcade import load_font

from resources import setup
from .navigation import navigation
from .window import Window
from .views import MenuView


def main():
    win = Window()
    setup()
    navigation.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
