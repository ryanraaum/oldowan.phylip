from oldowan.phylip import phylip
from nose.tools import raises

import os

SIMPLE_TEXT = """10 60
Cow       ATGGCATATCCCATACAACTAGGATTCCAAGATGCAACATCACCAATCATAGAAGAACTA
Carp      ATGGCACACCCAACGCAACTAGGTTTCAAGGACGCGGCCATACCCGTTATAGAGGAACTT
Chicken   ATGGCCAACCACTCCCAACTAGGCTTTCAAGACGCCTCATCCCCCATCATAGAAGAGCTC
Human     ATGGCACATGCAGCGCAAGTAGGTCTACAAGACGCTACTTCCCCTATCATAGAAGAGCTT
Loach     ATGGCACATCCCACACAATTAGGATTCCAAGACGCGGCCTCACCCGTAATAGAAGAACTT
Mouse     ATGGCCTACCCATTCCAACTTGGTCTACAAGACGCCACATCCCCTATTATAGAAGAGCTA
Rat       ATGGCTTACCCATTTCAACTTGGCTTACAAGACGCTACATCACCTATCATAGAAGAACTT
Seal      ATGGCATACCCCCTACAAATAGGCCTACAAGATGCAACCTCTCCCATTATAGAGGAGTTA
Whale     ATGGCATATCCATTCCAACTAGGTTTCCAAGATGCAGCATCACCCATCATAGAAGAGCTC
Frog      ATGGCACACCCATCACAATTAGGTTTTCAAGACGCAGCCTCTCCAATTATAGAAGAATTA
"""

SIMPLE_FILEPATH = os.path.join(os.path.dirname(__file__),
        'test_files', 'simple.phylip')
INTERLEAVED_FILEPATH = os.path.join(os.path.dirname(__file__),
        'test_files', 'interleaved.phylip')


def test_mode_accessor():
    """test mode accessor"""

    ff = phylip(SIMPLE_TEXT, 's')
    assert ff.mode == 's'

    ff = phylip(SIMPLE_FILEPATH, 'r')
    assert ff.mode == 'rU'


@raises(ValueError)
def test_bad_mode_string():
    """pass unknown mode string to phylip"""

    ff = phylip(SIMPLE_TEXT, 'q')


@raises(TypeError, ValueError)
def test_bad_mode_option():
    """pass non-string to mode option to phylip"""

    ff = phylip(SIMPLE_TEXT, 1)


@raises(ValueError)
def test_bad_value_to_write():
    """try to write entry without name"""

    ff = phylip(os.devnull, 'a')
    ff.write({'sequence': 'AGCT'})
    ff.close()


def test_basic_multi_entry_write():
    """try to write multiple entries"""

    entries = [{'name': 'a', 'sequence': 'A'}, {'name': 'g', 'sequence': 'G'}]
    ff = phylip(os.devnull, 'a')
    ff.write_entries(entries)
    ff.close()


def test_read_phylip_from_string():
    """read phylip given a string of phylip data"""

    # 's' is the 'string' mode
    ff = phylip(SIMPLE_TEXT, 's')
    entries = ff.readentries()
    ff.close()
    print entries
    assert 10 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'Cow' == entries[0]['name']
    assert 60 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'Carp' == entries[1]['name']
    assert 60 == len(entries[1]['sequence'])


def test_read_phylip_from_file():
    """read phylip given a filename"""

    ff = phylip(SIMPLE_FILEPATH, 'r')
    entries = ff.read()
    ff.close()
    assert 10 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'Cow' == entries[0]['name']
    assert 60 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'Carp' == entries[1]['name']
    assert 60 == len(entries[1]['sequence'])


def test_read_phylip_from_file_handle():
    """read phylip given an open file"""

    f = open(SIMPLE_FILEPATH, 'r')
    ff = phylip(f, 'f')
    entries = ff.readentries()
    ff.close()
    assert 10 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'Cow' == entries[0]['name']
    assert 60 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'Carp' == entries[1]['name']
    assert 60 == len(entries[1]['sequence'])


def test_iterate_phylip():
    """iterate phylip with parsing"""
    # first, from a string of phylip data
    for entry in phylip(SIMPLE_TEXT, 's'):
        assert isinstance(entry, dict)
    # next, from a filename with phylip data
    for entry in phylip(SIMPLE_FILEPATH):
        assert isinstance(entry, dict)


