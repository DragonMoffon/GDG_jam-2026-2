from resources import setup_resources

from .context import navigation
from .views.menu import MenuView
from .window import Window


def main():
    win = Window()
    setup_resources()
    navigation.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
