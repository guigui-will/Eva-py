from __future__ import annotations
import ctypes
from typing import TYPE_CHECKING, Callable, Any

from .enum import ValueType
from .nil import EvaNil
from .ffi import EvaValue

if TYPE_CHECKING:
    from .list import EvaList
    from .map import EvaMap

EvaTypes = str | float | bool | EvaNil | 'EvaList' | 'EvaMap'


def make_value_from(ptr: ctypes.POINTER(EvaValue)) -> EvaTypes:  # type: ignore[valid-type]
    """Convert a raw EvaValue pointer into the appropriate Python type."""
    from .list import EvaList
    from .map import EvaMap

    val: EvaValue = ptr.contents
    tag = val.tag

    if tag == ValueType.EVA_BOOL:
        return bool(val.data.boolean)

    if tag == ValueType.EVA_NUMBER:
        return val.data.number

    if tag == ValueType.EVA_NIL:
        return EvaNil()

    if tag == ValueType.EVA_STRING:
        raw = val.data.string
        return raw.decode('utf-8') if raw else ''

    if tag == ValueType.EVA_LIST:
        return EvaList(ptr)

    if tag == ValueType.EVA_MAP:
        return EvaMap(ptr)

    raise ValueError(f'Unknown EVA tag: {tag}')

# tem que olhar isso aí direitinho 