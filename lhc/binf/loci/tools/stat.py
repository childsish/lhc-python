from argparse import ArgumentParser, Namespace
from typing import Iterable
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io.loci import open_loci_file


def stat(loci: Iterable[GenomicInterval]):
    ends = {}
    insert_sizes = {}
    for locus in loci:
        gene_id = locus.data['transcript_id']
        if gene_id in ends:
            insert_sizes.setdefault(gene_id, []).append(locus.start - ends[gene_id])
        ends[gene_id] = locus.stop
    return insert_sizes


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> ArgumentParser:
    return define_parser(ArgumentParser())


def define_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.set_defaults(func=init_stat)
    return parser


def init_stat(args: Namespace):
    with open_loci_file(args.input) as fileobj:
        mn = 0
        mx = 0
        for k, vs in stat(fileobj).items():
            for v in vs:
                if v < mn:
                    mn = v
                elif v > mx:
                    mx = v
        print('{}\t{}'.format(mn, mx))


if __name__ == '__main__':
    main()
