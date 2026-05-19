from __future__ import annotations
import os

from .errors import errors
from .ffi import _libeva, _wrapper, library_path, cstr, EvaParser
from .nil import EvaNil
from .list import EvaList
from .map import EvaMap
from .values import make_value_from, EvaTypes


class Eva:
    def __init__(self, filepath: str) -> None:
        self.path = filepath
        self.filename = os.path.basename(filepath)

        self._driver = _libeva.eva_make_parser(filepath.encode('utf-8'))

        _wrapper.eva_wrapper_load_library(library_path.encode('utf-8'))

        if not self._driver:
            raise RuntimeError('Failed to spawn the Eva parser')

        status = self._driver.contents.status
        if status != 0:
            msg = errors.get(status, lambda s: 'Unknown error')(self)
            raise RuntimeError(msg)

    def get(self, namespace: str, field: str) -> EvaTypes:
        exists = _libeva.eva_check_exist_field_in_namespace(
            self._driver, cstr(namespace), cstr(field)
        )
        if not exists:
            raise KeyError(f"Field '{field}' does not exist in namespace '{namespace}'")

        ptr = _wrapper.eva_get_value_from_namespace_wrapper(
            self._driver, cstr(namespace), cstr(field)
        )
        if not ptr:
            raise RuntimeError('Failed to get value from namespace')

        return make_value_from(ptr)


__all__ = ['Eva', 'EvaNil', 'EvaList', 'EvaMap', 'EvaTypes']
