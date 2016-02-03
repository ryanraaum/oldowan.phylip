"""This is the oldowan.phylip package."""


import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
               'VERSION')).read().strip()

__all__ = ['phylip']

try:
    from oldowan.phylip.phylip import phylip
except:
    from phylip import phylip
