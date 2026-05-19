from __future__ import annotations
import ctypes
from typing import List

from .ffi import EvaValue, _wrapper
from .nil import EvaNil


class EvaList:
    def __init__(self, ptr: ctypes.POINTER(EvaValue)) -> None:  # type: ignore[valid-type]
        self._ptr = ptr
        self.length: int = _wrapper.eva_get_list_length_wrapper(ptr)

    def list(self) -> list:
        return [self.get(i) for i in range(self.length)]

    def get(self, i: int):
        from .values import make_value_from
        if i < 0 or i >= self.length:
            return EvaNil()
        ptr = _wrapper.eva_get_list_field_wrapper(self._ptr, i)
        if not ptr:
            raise RuntimeError('Failed to get value from list')
        return make_value_from(ptr)

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        for i in range(self.length):
            yield self.get(i)

    def __repr__(self) -> str:
        return f'[Eva list of length {self.length}]'

    def __str__(self) -> str:
        return repr(self)
