import argparse
import gzip
import os

from lhc.io.fastq import iter_fastq
from lhc.misc.bitap import bitap_fuzzy


def filter(read_files, filters, mode='all', output_dir=None):
    fn = all if mode == 'all' else\
        any if mode == 'any' else\
        None
    input_streams = [iter_fastq(gzip.open(read_file, 'rt') if read_file.endswith('.gz') else
                                open(read_file)) for read_file in read_files]

    output_names = [read_file.rsplit('.', 2)[0] if read_file.endswith('.gz') else
                    read_file.rsplit('.', 1)[0] for read_file in read_files]
    if output_dir is not None:
        output_names = [os.path.join(output_dir, os.path.basename(output_name)) for output_name in output_names]

    output_streams = [gzip.open('{}.filtered.fastq.gz'.format(output_name), 'w') for output_name in output_names]
    for i, reads in enumerate(zip(*input_streams)):
        if i % 10000 == 0:
            print(i)
        if fn(bitap_fuzzy(query, reads[index].seq, mismatches) is not None for query, mismatches, index in filters):
            for read, output_stream in zip(reads, output_streams):
                output_stream.write(str(read).encode('utf-8'))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(
        'Filters synchronised (eg. single-/paired-end) fastq files for the presence of any or all of the filter'
        ' sequences. Consider using "agrep" instead.'))


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('read_files', nargs='+')
    parser.add_argument('-f', '--filter', dest='filters', nargs=3, action='append',
                        metavar=('SEQUENCE', 'MISMATCHES', 'INDEX'), required=True)
    parser.add_argument('-m', '--mode', choices=['all', 'any'], default='all')
    parser.add_argument('-o', '--output-dir')
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    filters = [(sequence, int(mismatches), int(index)) for sequence, mismatches, index in args.filters]
    filter(args.read_files, filters, args.mode, args.output_dir)


if __name__ == '__main__':
    import sys
    sys.exit(main())
