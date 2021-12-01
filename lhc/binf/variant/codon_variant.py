from dataclasses import dataclass


@dataclass
class CodonVariant:
    pos: int
    ref: str
    alt: str
    fs: int = 0

    def __str__(self):
        if self.fs == 0:
            return 'c.{}{}>{}'.format(self.pos + 1, self.ref, self.alt)
        else:
            return 'c.{}{}{}fs{}'.format(self.ref[:3], self.pos + 1, self.alt[:3], 'Ter' + str(self.fs) if self.alt[-3:].upper() in {'TAA', 'TAG', 'TGA'} else '*?')
