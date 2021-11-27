from dataclasses import dataclass
from typing import Optional


@dataclass
class CodonVariant:
    pos: int
    ref: str
    alt: str
    fs: int = 0

    def __str__(self):
        return 'c.{}{}>{}'.format(self.pos, self.ref, self.alt)
