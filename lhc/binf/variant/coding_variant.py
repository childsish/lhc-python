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
            rng = str(pos + len(alt) - 1) if d == 1 else '{}_{}'.format(pos + len(alt) - d, pos + len(alt) - 1)
            res.append('{}:c.{}ins{}'.format(self.id, rng, alt))
        else:
            if len(ref) > 1 and ref == alt[::-1]:
                res.append('{}:c.{}_{}inv'.format(self.id, pos + 1, pos + len(ref)))
            else:
                res.append('{}:c.{}{}>{}'.format(self.id, pos + 1, ref, alt))
        return ','.join(res)


def call_coding_variants(nucleotide_variants, loci):
    assert all(loci[i] < loci[i + 1] for i in range(len(loci) - 1))

    nucleotide_variant_iterator = iter(nucleotide_variants)
    locus_iterator = iter(loci)
    nucleotide_variant = next(nucleotide_variant_iterator)
    locus = next(locus_iterator)

    coding_variants = []
    while nucleotide_variant is not None and locus is not None:
        if nucleotide_variant.pos < locus.start:
            coding_variants.append(None)
            nucleotide_variant = next(nucleotide_variant_iterator, None)
        elif nucleotide_variant.pos >= locus.stop:
            locus = next(locus_iterator, None)
        else:
            coding_position = locus.get_rel_pos(nucleotide_variant.pos)
            coding_variants.append(CodingVariant(locus.data['product'], coding_position, nucleotide_variant.ref, nucleotide_variant.alt))
            nucleotide_variant = next(nucleotide_variant_iterator, None)

    while nucleotide_variant is not None:
        coding_variants.append(None)
        nucleotide_variant = next(nucleotide_variant_iterator, None)

    return coding_variants
