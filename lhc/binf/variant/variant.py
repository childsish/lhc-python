from dataclasses import dataclass
from typing import Optional


@dataclass
class Variant:
    pos: int
    ref: str
    alt: str
    id: Optional[str] = None
    qual: Optional[float] = None
    filter: Optional[str] = None
    info: Optional[str] = None
    format: Optional[str] = None
    samples: Optional[list] = None

    def __str__(self):
        if self.alt[0] == '-':
            return 'g.{}_{}del'.format(self.pos, self.pos + len(self.ref))
        elif self.ref[0] == '-':
            return 'g.{}_{}ins{}'.format(self.pos, self.pos + 1, self.alt)
        return 'g.{}{}>{}'.format(self.pos, self.ref, self.alt)
