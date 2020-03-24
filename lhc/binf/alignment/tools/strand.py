import pysam

from collections import Counter
from argparse import ArgumentParser


def strand(alignments: pysam.AlignmentFile):
    counter = Counter()
    i = 0
    try:
        for alignment in alignments:
            if i > 100000:
                break
            if alignment.is_read2:
                continue
            read_strand = 'FR'[alignment.is_reverse]
            mate_strand = 'FR'[alignment.mate_is_reverse]
            counter['{}{}{}'.format(alignment.is_paired, read_strand, mate_strand)] += 1
            i += 1
    except KeyboardInterrupt:
        pass
    return counter


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(ArgumentParser())


def define_parser(parser):
    parser.add_argument('input')
    parser.set_defaults(func=init_strand)
    return parser


def init_strand(args):
    print(strand(pysam.AlignmentFile(args.input)))


if __name__ == '__main__':
    main()
