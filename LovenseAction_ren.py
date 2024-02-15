from enum import Enum
import enum

"""renpy
init -1 python:
"""


class LovenseAction(Enum):
    VIBRATE = enum.auto()
    ROTATE = enum.auto()
    PUMP = enum.auto()
    THRUST = enum.auto()
    FINGER = enum.auto()
    SUCTION = enum.auto()
    DEPTH = enum.auto()
    ALL = enum.auto()
    STOP = enum.auto()
