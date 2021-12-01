from dataclasses import dataclass


@dataclass
class AminoAcidVariant:
    pos: int
    ref: str
    alt: str
    fs: int = 0

    def __str__(self):
        pos = self.pos
        ref = self.ref
        alt = self.alt
        if self.fs > 0:
            res = 'p.{}{}{}fs{}'.format(self.ref[0], self.pos + 1, self.alt[0], 'Ter' + str(self.fs) if self.alt[-1] == '*' else '*?')
        elif len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = pos + 1 if d == 1 else '{}_{}'.format(pos + 1, pos + len(ref) - 1)
            res = 'p.{}del'.format(rng)
        elif len(alt) > len(ref):
            res = 'p.{}_{}ins{}'.format(pos + 1, pos + 2, alt)
        else:
            res = 'p.{}{}{}'.format(self.ref, pos + 1, alt)
        return res
