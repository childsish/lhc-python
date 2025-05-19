import pysam

from lhc.entities import Locus


class TabixFileWrapper:
    def __init__(self, filename: str):
        self.index = pysam.TabixFile(filename)

    def __getitem__(self, item: Locus):
        return self.index.fetch(item.chromosome, item.start.position, item.end.position)
