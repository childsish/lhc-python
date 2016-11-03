#!/usr/bin/python

import argparse
import gzip
import sys

from ..merger import VcfMerger


def merge(fnames, out, bams):
    merger = VcfMerger(fnames, bams=bams)
    for key, values in merger.hdrs.items():
        for value in values:
            out.write('##{}={}\n'.format(key, value))
    out.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t' + '\t'.join(merger.samples) + '\n')
    for entry in merger:
        format = sorted(key for key in iter(entry.data['samples'].values()).next().keys() if key != '.') if \
            len(entry.data['samples']) > 0 else []
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            entry.chromosome,
            entry.position + 1,
            entry.data['id'],
            entry.data['ref'],
            ','.join(entry.data['alt']),
            entry.data['qual'],
            entry.data['filter'],
            entry.data['info'],
            ':'.join(format),
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
    inputs = [gzip.open(i, 'rt') if i.endswith('gz') else open(i) for i in args.inputs]
    output = sys.stdout if args.output is None else open(args.output)
    merge(inputs, output, args.bams)


if __name__ == '__main__':
    sys.exit(main())
