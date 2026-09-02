# ? Now that I understand Paramspec we can make notifications way nicer
from __future__ import annotations

from collections.abc import Callable
from types import MethodType
from typing import Any, Self
from weakref import WeakMethod, ref


type _NotifMethod[**P] = Callable[P, Any]
type _NotifMethodWeak[**P] = ref[_NotifMethod[P]]

class notification[**P]:

    def __init__(self, _param: _NotifMethod[P]) -> None:
        self._bound: _NotifMethodWeak[P] = self._make_weak(_param, ephemiral=True)
        self.observers: dict[_NotifMethodWeak[P], None] = {}

    def __get__(self, instance, cls=None) -> Self:
        # TODO: per-instance notifications?
        return self

    def _make_weak(self, function: _NotifMethod[P], ephemiral: bool = False) -> ref[_NotifMethod]:
        callback = None if ephemiral else self._rem_observer
        return WeakMethod(function, callback) if isinstance(function, MethodType) else ref(function, callback)

    def _rem_observer(self, callback: _NotifMethodWeak[P]):
        self.observers.pop(callback, None)

    def emit(self, *args: P.args, **kwds: P.kwargs):
        for observer in self.observers:
            if (callback := observer()) is None:
                self._rem_observer(observer)
            else:
                callback(*args, **kwds)

    __call__ = emit

    def attach(self, observer: _NotifMethod[P]):
        ref = self._make_weak(observer)
        self.observers[ref] = None # We are using a dictionary as an ordered set

    def detach(self, observer: _NotifMethod[P]):
        ref = self._make_weak(observer, ephemiral=True)
        self._rem_observer(ref)


@notification
def example(a: float, b: float): ...
