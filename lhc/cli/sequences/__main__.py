import os

from lhc.misc.argparse import main_with_tools


if __name__ == '__main__':
    import sys
    sys.exit(main_with_tools(
        os.path.join(os.path.dirname(__file__), 'tools'),
        'lhc.binf.sequences.tools',
        description='Tools for working with sets of sequences.'
    ))