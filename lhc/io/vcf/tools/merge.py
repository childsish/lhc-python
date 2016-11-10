#!/usr/bin/python

import argparse
import gzip
import os
import sys

from lhc.order import natural_key
from ..iterator import VcfIterator
from ..merger import VcfMerger


def merge(iterators, out, bams, *, natural_order=False):
    key = natural_key if natural_order else None
    merger = VcfMerger(iterators, bams=bams, key=key)
    for key, values in merger.hdrs.items():
        for value in values:
            out.write('##{}={}\n'.format(key, value))
    out.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO')
    if len(merger.samples) > 0:
        out.write('\tFORMAT\t{}'.format('\t'.join(merger.samples)))
    out.write('\n')
    for entry in merger:
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            entry.chromosome,
            entry.position + 1,
            entry.data['id'],
            entry.data['ref'],
            ','.join(entry.data['alt']),
            '.' if entry.data['qual'] is None else entry.data['qual'],
            entry.data['filter'],
            ':'.join('{}={}'.format(k, ','.join(vs)) for k, vs in entry.data['info'].items()),
            ':'.join(entry.data['format']),
            '\t'.join('.' if sample in entry.data['samples'] and '.' in entry.data['samples'][sample] else
                      ':'.join(entry.data['samples'][sample][f] for f in format) if sample in entry.data['samples'] else '.'
                      for sample in merger.samples)
        ))
    out.close()


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('inputs', nargs='+')
    add_arg('-b', '--bams', nargs='+',
            help='Include read counts from bam files')
    add_arg('-o', '--output',
            help='Name of the merged vcf_ (default: stdout).')
    add_arg('-n', '--natural_order', action='store_true', default=False,
            help='Chromosome names are in natural order (default: false)')
    parser.set_defaults(func=init_merge)
    return parser


def init_merge(args):
    inputs = [VcfIterator(fileobj) for fileobj in
              (gzip.open(i, 'rt') if i.endswith('gz') else
               open(i) for i in args.inputs)]
    names = trim_names(args.inputs)
    for name, input in zip(names, inputs):
        if len(input.samples) == 0:
            input.samples.append(name)
    output = sys.stdout if args.output is None else open(args.output)
    merge(inputs, output, args.bams, natural_order=args.natural_order)


def trim_names(inputs):
    inputs = [os.path.basename(input) for input in inputs]
    smallest_name_length = min(len(input) for input in inputs)
    i = 1
    while i < smallest_name_length:
        if len(set(input[-i] for input in inputs)) > 1:
            break
        i += 1
    return [input[:-i] for input in inputs]


if __name__ == '__main__':
    sys.exit(main())
