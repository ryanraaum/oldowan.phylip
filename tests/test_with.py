from __future__ import with_statement

import os

from oldowan.phylip import phylip

SIMPLE_FILEPATH = os.path.join(os.path.dirname(__file__), 
        'test_files', 'simple.phylip')

def test_with():
    """test of with statement hooks"""
    with phylip(SIMPLE_FILEPATH, 'r') as f:
        for entry in f:
            assert isinstance(entry, dict)
    assert f.closed
