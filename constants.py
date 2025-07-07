from enum import Enum


class PressPurpose(Enum):
    MOVE = 1,
    RESIZE = 2,
    CONTEXT_MENU = 3,
    NONE = 4,


class ReaderConstants:
    CONTENT_SCROLL_RIGHT_MARGIN = 150
