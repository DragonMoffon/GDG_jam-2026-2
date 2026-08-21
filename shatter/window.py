from arcade import Window as ArcadeWindow


class Window(ArcadeWindow):
    def __init__(self):
        super().__init__(1280, 720, "Shatter -- GDG Jam 2026-2 --")
