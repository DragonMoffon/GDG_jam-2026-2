from resources import setup_resources

from .context import navigation, setup_manager
from .views_old import MenuView
from .window import Window


def main():
    win = Window()
    setup_resources()
    setup_manager()
    navigation.setup(MenuView(), win)
    win.run()


if __name__ == "__main__":
    main()
