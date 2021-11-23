import string

from lhc.binf.genomic_coordinate import GenomicPosition, NestedGenomicInterval
from lhc.tools import Tokeniser, Token
from .locus_file import LocusFile
from typing import List, Optional


class EmblFile(LocusFile):

    EXTENSION = ('.embl', '.embl.gz')
    FORMAT = 'embl'

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8', index=1):
        super().__init__(filename, mode, encoding, index)
        self.tokeniser = Tokeniser(
            {
                'digit': string.digits,
                'word': string.ascii_letters + '_.^',
                'bracket': '()',
                'separator': ',:',
                'unknown': '<>',
            },
            individual={'(', ')'}
        )

    def iter(self):
        line = next(self.file)
        while not line.startswith(';FT'):
            line = next(self.file)
        while line.startswith(';FT'):
            raw_entry = [line]
            raw_entry.extend(line for line in self.file if len(line) > 7 and line[6] == ' ')
            yield raw_entry
            line = next(self.file, '')

    def parse(self, lines: List[str], index=1) -> NestedGenomicInterval:
        interval = self.parse_location(lines[0][21:].strip())
        interval.data = self.parse_qualifiers(lines[1:])
        return interval

    def parse_location(self, location_definition: str) -> NestedGenomicInterval:
        tokens = list(self.tokeniser.tokenise(location_definition))
        return self.parse_nested_interval(tokens)

    def parse_nested_interval(self, tokens: List[Token]) -> NestedGenomicInterval:
        """ Parses a super range.
         SuperRange ::= Interval | Join | Complement
        """
        if tokens[0].type in {'digit', 'unknown'}:
            return self.parse_interval(tokens)
        elif tokens[0].value in ['join', 'order']:
            return self.parse_join(tokens)
        elif tokens[0].value == 'complement':
            return self.parse_complement(tokens)
        elif tokens[1].value == ':':
            chromosome = tokens.pop(0).value
            tokens.pop(0)  # pop ':'
            return self.parse_interval(tokens, chromosome=chromosome)
        raise ValueError('interval {} does not fit pattern.'.format(tokens))

    def parse_interval(self, tokens: List[Token], chromosome=None) -> NestedGenomicInterval:
        """ Parses an interval
         Range ::= <num> | <num> ('..' | '^' | '.') <num>
        """
        fr = self.parse_digit(tokens) - 1
        if len(tokens) > 1 and tokens[0].value in {'..', '^', '.'}:
            tokens.pop(0)  # Pop '..' | '^' | '.'
            to = self.parse_digit(tokens)
            return NestedGenomicInterval(fr, to, chromosome=chromosome)
        return NestedGenomicInterval(fr, fr + 1, chromosome=chromosome)

    def parse_digit(self, tokens: List[Token]) -> GenomicPosition:
        token = tokens.pop(0)
        if token.value in '<>':
            token = tokens.pop(0)
        return GenomicPosition(int(token.value))

    def parse_join(self, tokens: List[Token]) -> NestedGenomicInterval:
        """ Parses a join.
         Join ::= 'join' '(' NestedInterval [',' NestedInterval] ')'
        """
        tokens.pop(0)  # Pop 'join'
        tokens.pop(0)  # Pop '('
        child = self.parse_nested_interval(tokens)
        parent = NestedGenomicInterval(child.start.position, child.stop.position)
        parent.add_child(child)
        while tokens[0].value == ',':
            tokens.pop(0)
            parent.add_child(self.parse_nested_interval(tokens))
        tokens.pop(0)  # Pop ')'
        return parent

    def parse_complement(self, tokens: List[Token]) -> NestedGenomicInterval:
        """ Parses a complement
         Complement ::= 'complement' '(' NestedInterval ')'
        """
        tokens.pop(0)  # Pop 'complement'
        tokens.pop(0)  # Pop '('
        res = self.parse_nested_interval(tokens)
        res.switch_strand()
        tokens.pop(0)  # Pop ')'
        return res

    def parse_qualifiers(self, lines):
        qualifiers = {}
        i = 0
        while i < len(lines) and lines[i][20] == '/':
            key, value = lines[i][21:].strip().split('=')
            if value.startswith('"') and not value.endswith('"'):
                values = [value]
                while not values[-1].endswith('"'):
                    i += 1
                    values.append(lines[i][20:].strip())
                value = ''.join(values)
            i += 1
            if value.startswith('"'):
                value = value[1:-1]
            elif value.isdigit():
                value = int(value)
            qualifiers[key] = value
        return qualifiers

    def format(self, interval: NestedGenomicInterval, index=1) -> str:
        raise NotImplementedError()
