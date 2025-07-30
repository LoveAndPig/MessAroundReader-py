from enum import Enum


class PressPurpose(Enum):
    MOVE = 1,
    RESIZE = 2,
    CONTEXT_MENU = 3,
    NONE = 4,


class ShorCutTarget(Enum):
    PREVIOUS_LINE = 1,
    NEXT_LINE = 2,
    MOVE_BACKWARD = 3,
    MOVE_FORWARD = 4,
    NONE = 5,


class ReaderConstants:
    CONTENT_SCROLL_RIGHT_MARGIN = 150
    LONG_SCROLL_BRAKE = 6
    SHORT_SCROLL_BRAKE = 2
