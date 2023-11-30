from enum import Enum


class PromptType(Enum):
    CLICK = 'click'
    BOX = 'box'
    DOODLE = 'brush'
    MASK = 'mask'
    DEFAULT = 'mouse'


RADIUS = 10