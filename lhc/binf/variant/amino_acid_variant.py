from dataclasses import dataclass
from typing import Optional


@dataclass
class AminoAcidVariant:
    pos: int
    ref: str
    alt: str
    fs: Optional[int]

    def __str__(self):
        res = []
        pos = self.pos
        ref = self.ref
        alt = self.alt
        fs = self.fs
        if len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = str(pos + len(ref) - 1,) if d == 1 else '{}_{}'.format(pos + len(ref) - d, pos + len(ref) - 1)
            r = 'p.{}del{}'.format(rng, ref[-d - 1:-1])
        elif len(alt) > len(ref):
            d = len(alt) - len(ref)
            typ = 'dup' if alt[-d - 1:-1] == ref[-d - 1:-1] else 'ins'
            rng = str(pos + len(alt) - 1,) if d == 1 else '{}_{}'.format(pos + len(alt) - d, pos + len(alt) - 1)
            r = 'p.{}{}{}'.format(rng, typ, alt[-d - 1:-1])
        else:
            i = 0
            j = len(ref) - 1
            if ref != alt:
                while ref[i] == alt[i]:
                    i += 1
                while ref[j] == alt[j]:
                    j -= 1
                j += 1
            r = 'p.{}{}{}'.format(ref[i:j + 1], pos + i + 1, alt[i:j + 1])
            if fs is not None:
                r += 'fs*{}'.format(int(fs))
        res.append(r)
        return ','.join(res)
