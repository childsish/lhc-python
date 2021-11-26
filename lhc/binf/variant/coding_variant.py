from dataclasses import dataclass


@dataclass
class CodingVariant:
    id: str
    pos: int
    ref: str
    alt: str

    def __str__(self):
        res = []
        pos = self.pos
        ref = self.ref
        alt = self.alt
        if len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = str(pos + len(ref) - 1,) if d == 1 else '{}_{}'.format(pos + len(ref) - d, pos + len(ref) - 1)
            res.append('{}:c.{}del'.format(self.id, rng))
        elif len(alt) > len(ref):
            d = len(alt) - len(ref)
            typ = 'dup' if alt[-d - 1:-1] == ref[-d - 1:-1] else 'ins'
            rng = str(pos + len(alt) - 1,) if d == 1 else '{}_{}'.format(pos + len(alt) - d, pos + len(alt) - 1)
            res.append('{}:c.{}{}{}'.format(self.id, rng, typ, alt[-d - 1:-1]))
        else:
            if len(ref) > 1 and ref == alt[::-1]:
                res.append('{}:c.{}_{}inv'.format(self.id, pos + 1, pos + len(ref)))
            else:
                res.append('{}:c.{}{}>{}'.format(self.id, pos + 1, ref, alt))
        return ','.join(res)
