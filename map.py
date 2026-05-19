from __future__ import annotations
import ctypes

from .ffi import EvaValue, _wrapper, cstr
from .nil import EvaNil


class EvaMap:
    def __init__(self, ptr: ctypes.POINTER(EvaValue)) -> None:  # type: ignore[valid-type]
        self._ptr = ptr
        self.length: int = _wrapper.eva_get_map_length_wrapper(ptr)

    def keys(self) -> 'EvaList':
        from .list import EvaList
        ptr = _wrapper.eva_get_all_keys_from_map_wrapper(self._ptr)
        if not ptr:
            raise RuntimeError('Failed to get keys from map')
        return EvaList(ptr)

    def get(self, key: str):
        from .values import make_value_from
        if not _wrapper.eva_check_exist_field_in_map_wrapper(self._ptr, cstr(key)):
            return EvaNil()
        ptr = _wrapper.eva_get_map_field_wrapper(self._ptr, cstr(key))
        if not ptr:
            raise RuntimeError('Failed to get value from map')
        return make_value_from(ptr)

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return f'[Eva map of length {self.length}]'

    def __str__(self) -> str:
        return repr(self)
