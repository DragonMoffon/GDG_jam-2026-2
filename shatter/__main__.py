from resources import setup

from .navigation import navigation
from .views import MenuView
from .window import Window


def main():
    win = Window()
    setup()
    navigation.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
