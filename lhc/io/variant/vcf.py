from collections import OrderedDict
from typing import Any, Dict, Iterator
from .variant_file import Variant, VariantFile


class VcfFile(VariantFile):

    EXTENSION = ('.vcf', '.vcf.gz')
    FORMAT = 'vcf'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = []
        self.sample_names = []

    def iter(self) -> Iterator[str]:
        line = next(self.file)
        while line.startswith('##'):
            self.header.append(line)
            line = next(self.file)
        self.sample_names = line.strip().split('\t')[9:]
        for line in self.file:
            yield line

    def parse(self, line: str, index=1) -> Variant:
        parts = line.rstrip('\r\n').split('\t')
        info = dict(i.split('=', 1) if '=' in i else (i, i) for i in parts[7].split(';'))
        format = None if len(parts) < 9 else parts[8].split(':')
        return Variant(
            parts[0],
            int(parts[1]) - 1,
            parts[3],
            parts[4].split(',')[0],
            parts[2],
            get_float(parts[5]),
            parts[6].split(',')[0],
            info,
            format,
            self.get_samples(parts[9:], format))

    def format(self, variant: Variant, index=1) -> str:
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            str(variant.chr),
            variant.pos + index,
            variant.id,
            variant.ref,
            ','.join(variant.alt),
            '.' if variant.qual is None else variant.qual,
            ','.join(variant.filter),
            ':'.join('{}={}'.format(k, v) for k, v in variant.info.items()),
            ':'.join(variant.format),
            '\t'.join(self.format_sample(variant.samples[sample], variant.format)
                      if sample in variant.samples
                      else '.' for sample in variant.samples)
        )

    def get_samples(self, parts, format) -> Dict[str, Any]:
        samples = {}
        for name, part in zip(self.sample_names, parts):
            samples[name] = {} if part == '.' else dict(zip(format, part.split(':')))
        return samples

    @staticmethod
    def format_sample(sample, format):
        return ':'.join(sample[key] for key in format)


def get_header(iterator):
    header = OrderedDict()
    line = next(iterator)
    while line.startswith('##'):
        key, value = line[2:].strip().split('=', 1)
        if key not in header:
            header[key] = set()
        header[key].add(value)
        line = next(iterator)
    samples = line.rstrip('\r\n').split('\t')[9:]
    return header, samples


def get_float(string):
    try:
        return float(string)
    except:
        pass
