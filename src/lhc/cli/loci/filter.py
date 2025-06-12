import sys
import argparse

from typing import Iterable, Iterator, Optional, Set
from lhc.entities.locus import Locus
from lhc.io.locus import open_locus_file


def filter(
    loci: Iterable[Locus],
    filter_: Optional[str] = None,
    gene_list: Optional[Set[str]] = None,
    inverse: bool = False
) -> Iterator[Locus]:
    local_variables = {}
    if gene_list is not None:
        local_variables['gene_list'] = set(gene_list)
    
    filter_fn = eval('lambda: {}'.format(filter_)) if filter_ else lambda: True
    
    for locus in loci:
        local_variables.update({
            'chromosome': locus.chromosome,
            'start': locus.interval.start,
            'end': locus.interval.end,
            'strand': locus.strand
        })
        if locus.data:
            local_variables.update(locus.data)
        globals().update(local_variables)
        match = filter_fn()
        if inverse:
            match = not match
        if match:
            yield locus


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Filter loci using the given conditions.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be filtered (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the filtered intervals file (default: stdout).')
    parser.add_argument('-f', '--filter', required=True,
                        help='filter to apply (default: none).')
    parser.add_argument('-g', '--gene-list',
                        help='File with list of newline separated gene names. Made available to filter as `gene_list`.')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-v', '--inverse', action='store_true',
                        help='invert filter.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--region',
                       help='apply filter in region (default: none).')
    group.add_argument('-x', '--exclude',
                       help='do not apply filter in region (default: none).')
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    gene_list = None
    if args.gene_list:
        with open(args.gene_list) as fileobj:
            gene_list = set(line.strip() for line in fileobj if line.strip())
            
    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        for interval in filter(input, args.filter, gene_list, args.inverse):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
