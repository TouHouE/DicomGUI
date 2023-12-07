from enum import Enum


class PromptType(Enum):
    CLICK = 'click'
    BOX = 'box'
    DOODLE = 'brush'
    MASK = 'mask'
    DEFAULT = 'mouse'

    def is_spare_prompt(self, prompt: 'PromptType'):
        return prompt == PromptType.CLICK or prompt == PromptType.BOX or prompt == PromptType.DOODLE
RADIUS = 10