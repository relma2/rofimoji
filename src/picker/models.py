import enum
from dataclasses import dataclass


class Action(enum.Enum):
    TYPE = "type"
    COPY = "copy"
    CLIPBOARD = "clipboard"
    UNICODE = "unicode"
    COPY_UNICODE = "copy-unicode"
    STDOUT = "print"
    MENU = "menu"

    def __str__(self):
        return self.value


class CANCEL:
    def __eq__(self, other):
        return isinstance(other, CANCEL)


class DEFAULT:
    def __eq__(self, other):
        return isinstance(other, DEFAULT)


@dataclass
class Shortcut:
    index: int
