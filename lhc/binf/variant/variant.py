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
    lead: Optional[str] = None

    def __str__(self):
        res = []
        pos = self.pos
        ref = self.ref
        alt = self.alt
        if len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = str(pos + len(ref) - 1,) if d == 1 else '{}_{}'.format(pos + len(ref) - d, pos + len(ref) - 1)
            res.append('g.{}del'.format(rng))
        elif len(alt) > len(ref):
            d = len(alt) - len(ref)
            typ = 'dup' if alt[-d - 1:-1] == ref[-d - 1:-1] else 'ins'
            rng = str(pos + len(alt) - 1,) if d == 1 else '{}_{}'.format(pos + len(alt) - d, pos + len(alt) - 1)
            res.append('g.{}{}{}'.format(rng, typ, alt[-d - 1:-1]))
        else:
            if len(ref) > 1 and ref == alt[::-1]:
                res.append('g.{}_{}inv'.format(pos + 1, pos + len(ref)))
            else:
                res.append('g.{}{}>{}'.format(pos + 1, ref, alt))
        return ','.join(res)
