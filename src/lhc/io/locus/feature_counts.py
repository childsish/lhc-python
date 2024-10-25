from .locus_file import GenomicInterval, LocusFile


class FeatureCountsFile(LocusFile):

    EXTENSION = ('.txt', '.txt.gz')
    FORMAT = 'feature_counts'

    def parse_headers(self):
        line = next(self.file).strip('\r\n')
        while line.startswith('#'):
            line = next(self.file)
        return line.split('\t')

    def write_headers(self, locus):
        self.file.write(f'Geneid\tChr\tStart\tEnd\tStrand\tLength\t')
        self.file.write('\t'.join(locus.data['counts'].keys()))

    def parse(self, line: str, index=1) -> GenomicInterval:
        gene_id, chr, start, end, strand, length, *counts = line.rstrip('\r\n').split('\t')
        data = {
            'gene_id': gene_id,
            'length': length,
            'counts': {key: int(value) for key, value in zip(self.headers[6:], counts)}
        }
        return GenomicInterval(
            start,
            end,
            chromosome=chr,
            strand=strand,
            data=data)

    def format(self, interval: GenomicInterval, index=1) -> str:
        return f'{interval.data["gene_id"]}\t{interval.chromosome}\t{interval.start.position}\t{interval.stop.position}\t{interval.strand}\t{interval.data["length"]}\t' +\
            '\t'.join(str(count) for count in interval.data['counts'].values())
