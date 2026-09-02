from resources import setup

from .navigation import navigation
from .views_old import MenuView
from .window import Window


def main():
    win = Window()
    setup()
    navigation.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
