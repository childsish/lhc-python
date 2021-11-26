from dataclasses import dataclass


@dataclass
class CodonVariant:
    pos: int
    ref: str
    alt: str
    fs: int

    def __str__(self):
        return 'c.{}{}>{}'.format(self.pos, self.ref, self.alt)
