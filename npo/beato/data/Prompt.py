from npo.beato.constant import PromptType

class Prompt:
    def __init__(self):
        self.start_point = None
        self.tracking = []
        self.end_point = None

    def set_point(self, p):
        if self.start_point is None:
            self.start_point = p
            return

        if self.end_point is None:
            self.end_point = p
            return

        self.tracking.append(self.end_point)
        self.end_point = p

    def bbox(self):
        return {
            'start': self.start_point,
            'end': self.end_point if self.start_point is not None else self.tracking[-1]
        }

    def doodle(self):
        return {
            'start': self.start_point,
            'path': self.tracking,
            'end': self.end_point
        }

    def click(self):
        return self.start_point

    def mask(self):
        seq = [self.start_point]
        seq.extend(self.tracking)
        seq.append(self.end_point)

        return seq

    def clear(self):
        self.start_point = None
        self.tracking.clear()
        self.end_point = None

    def __getitem__(self, item):
        if item == PromptType.BOX:
            return self.bbox()
        elif item == PromptType.CLICK:
            return self.click()
        elif item == PromptType.DOODLE:
            return self.doodle()
        elif item == PromptType.MASK:
            return self.mask()

if __name__ == '__main__':
    p = Prompt()
    p.set_point([0, 1])
    out = p[PromptType.CLICK]
    print(out)
