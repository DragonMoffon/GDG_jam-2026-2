from arcade import View, Window, get_window


class NavigationStack:
    def __init__(self) -> None:
        self._stack: list[View]
        self._names: list[str | None]
        self._window: Window

    def setup(self, root: View, window: Window | None = None):
        self._stack = [root]
        self._names = ["root"]
        self._window = window if window is not None else get_window()
        self._window.show_view(root)

    @property
    def is_empty(self) -> bool:
        return not self._stack

    def push(self, view: View, name: str | None = None):
        self._stack.append(view)
        self._names.append(name)
        self._window.show_view(view)

    def pop(self, x: int = 1, *, until: str | None = None) -> View:
        if self.is_empty:
            raise ValueError("The navigation stack has run out of views.")
        if x == 0:
            return self._stack[-1]
        if until is not None:
            # Find name in stack and return TO that view
            for idx, name in enumerate(self._names[:0:-1]):
                if name == until:
                    return self.pop(idx)
            # If the name wasn't found, shortcut to clearing to "root"
            return self.pop(len(self._stack) - 1)

        # popping a large number is the same as returning to "root"
        x = min(x, len(self._stack) - 1)
        view = self._stack[-x]
        self._stack = self._stack[:-x]
        self._names = self._names[:-x]
        self._window.show_view(self.peek())  # Use peek to do is_empty check
        return view

    def peek(self, x: int = 1) -> View:
        if len(self._stack) < x:
            raise ValueError(f"The navigation stack has to few views to peek {x} times.")
        return self._stack[-x]

    def peek_name(self, x: int = 1) -> str | None:
        if len(self._stack) < x:
            raise ValueError(f"The navigation stack has to few views to peek {x} times.")
        return self._names[-x]

    def swap(self, view: View, name: str | None = None) -> None:
        if self.is_empty:
            raise ValueError("The navigation stack has run out of views.")
        self._stack[-1] = view
        self._names[-1] = name
        self._window.show_view(view)
