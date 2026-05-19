from enum import IntEnum

class ValueType(IntEnum):
    EVA_STRING = 0
    EVA_NUMBER = 1
    EVA_BOOL   = 2
    EVA_MAP    = 3
    EVA_LIST   = 4
    EVA_NIL    = 5
