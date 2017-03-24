import string
import unittest

from lhc.tools.tokeniser import Tokeniser


class TestTokeniser(unittest.TestCase):
    def test_tokeniser(self):
        tokeniser = Tokeniser({
            'number': '0123456789',
            'word': string.ascii_letters,
            'space': ' '
        })

        tokens = list(tokeniser.tokenise('19 out of 20'))

        self.assertEqual(7, len(tokens))
        self.assertEqual('number', tokens[0].type)
        self.assertEqual('19', tokens[0].value)
        self.assertEqual('space', tokens[1].type)
        self.assertEqual(' ', tokens[1].value)
        self.assertEqual('word', tokens[2].type)
        self.assertEqual('out', tokens[2].value)
        self.assertEqual('space', tokens[3].type)
        self.assertEqual(' ', tokens[3].value)
        self.assertEqual('word', tokens[4].type)
        self.assertEqual('of', tokens[4].value)
        self.assertEqual('space', tokens[5].type)
        self.assertEqual(' ', tokens[5].value)
        self.assertEqual('number', tokens[6].type)
        self.assertEqual('20', tokens[6].value)


if __name__ == '__main__':
    unittest.main()
