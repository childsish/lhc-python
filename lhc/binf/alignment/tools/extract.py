import argparse
import collections
import sys

from lhc.binf.loci.make_loci import make_loci
from lhc.io.alignment import open_alignment_file
from lhc.io.locus import open_locus_file


def extract(alignment, loci, filter_=None):
    filter_ = eval(f'lambda: {filter_}')
    for locus in loci:
        if filter_(locus):
            yield alignment.fetch(locus)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='alignment file (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='output fasta file (default: stdout).')
    parser.add_argument('-f', '--filter', required=True,
                        help='filter for loci')
    parser.add_argument('-l', '--loci', required=True,
                        help='loci to extract')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file.')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    with open_alignment_file(args.input, format=args.input_format) as alignments,\
            open_alignment_file(args.output, 'w', format=args.output_format) as output,\
            open_locus_file(args.sequence) as loci:
        if args.assemble:
            loci = make_loci(loci)
        sub_alignment_parts = collections.defaultdict(list)
        alignment = next(alignments)
        for sub_alignment in extract(alignment, loci, args.filter):
            for key, value in sub_alignment:
                sub_alignment_parts[key].append(value)
        sub_alignment = {key: ''.join(value) for key, value in sub_alignment_parts.items()}
        output.write(sub_alignment)


if __name__ == '__main__':
    sys.exit(main())
