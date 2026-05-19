import ctypes
import os
import platform
import sys

def _get_library_path() -> str:
    """Resolve the path to the native EVA shared library."""
    base = os.path.join(os.path.dirname(__file__), '..', 'eva')

    system = platform.system().lower()
    machine = platform.machine().lower()

    suffix_map = {'windows': 'dll', 'darwin': 'dylib'}
    suffix = suffix_map.get(system, 'so')

    # Match the TS naming: libeva-<platform>-<arch>.<suffix>
    name = f'libeva-{system}-{machine}.{suffix}'
    return os.path.realpath(os.path.join(base, name))


# C struct definitions 

class EvaValueData(ctypes.Union):
    _fields_ = [
        ('string',  ctypes.c_char_p),
        ('number',  ctypes.c_double),
        ('boolean', ctypes.c_int),
    ]

class EvaValue(ctypes.Structure):
    _fields_ = [
        ('tag',  ctypes.c_uint),
        ('data', EvaValueData),
    ]

class EvaParser(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_size_t),
        ('parser', ctypes.c_void_p),
    ]


# Load libraries 

library_path = _get_library_path()
_libeva: ctypes.CDLL = ctypes.CDLL(library_path)

# Compile/load wrapper.c at runtime is not straightforward in Python;
# instead we expose the same symbols directly from libeva.
# If a separate wrapper .so exists alongside libeva, load it too.
_wrapper_path = os.path.join(os.path.dirname(library_path), 'libeva_wrapper.so')
if os.path.exists(_wrapper_path):
    _wrapper: ctypes.CDLL = ctypes.CDLL(_wrapper_path)
else:
    _wrapper = _libeva  # symbols may be in the same lib


# Symbol bindings

# eva_make_parser(path: char*) -> EvaParser*
_libeva.eva_make_parser.restype  = ctypes.POINTER(EvaParser)
_libeva.eva_make_parser.argtypes = [ctypes.c_char_p]

# eva_check_exist_field_in_namespace(parser, ns, field) -> bool
_libeva.eva_check_exist_field_in_namespace.restype  = ctypes.c_bool
_libeva.eva_check_exist_field_in_namespace.argtypes = [
    ctypes.POINTER(EvaParser), ctypes.c_char_p, ctypes.c_char_p
]

# wrapper symbols
_wrapper.eva_wrapper_load_library.restype  = None
_wrapper.eva_wrapper_load_library.argtypes = [ctypes.c_char_p]

_wrapper.eva_get_value_from_namespace_wrapper.restype  = ctypes.POINTER(EvaValue)
_wrapper.eva_get_value_from_namespace_wrapper.argtypes = [
    ctypes.POINTER(EvaParser), ctypes.c_char_p, ctypes.c_char_p
]

_wrapper.eva_get_list_length_wrapper.restype  = ctypes.c_int
_wrapper.eva_get_list_length_wrapper.argtypes = [ctypes.POINTER(EvaValue)]

_wrapper.eva_get_list_field_wrapper.restype  = ctypes.POINTER(EvaValue)
_wrapper.eva_get_list_field_wrapper.argtypes = [ctypes.POINTER(EvaValue), ctypes.c_int]

_wrapper.eva_check_exist_field_in_map_wrapper.restype  = ctypes.c_bool
_wrapper.eva_check_exist_field_in_map_wrapper.argtypes = [ctypes.POINTER(EvaValue), ctypes.c_char_p]

_wrapper.eva_get_map_field_wrapper.restype  = ctypes.POINTER(EvaValue)
_wrapper.eva_get_map_field_wrapper.argtypes = [ctypes.POINTER(EvaValue), ctypes.c_char_p]

_wrapper.eva_get_map_length_wrapper.restype  = ctypes.c_int
_wrapper.eva_get_map_length_wrapper.argtypes = [ctypes.POINTER(EvaValue)]

_wrapper.eva_get_all_keys_from_map_wrapper.restype  = ctypes.POINTER(EvaValue)
_wrapper.eva_get_all_keys_from_map_wrapper.argtypes = [ctypes.POINTER(EvaValue)]


def cstr(s: str) -> bytes:
    return s.encode('utf-8') + b'\x00'
