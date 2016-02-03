Read and write PHYLIP format.

oldowan.phylip is a small bioinformatic utility to read and write sequence data
in the format used by the PHYLIP_ programs. This a simple file format for
storing multiple DNA, RNA, or protein sequences in a single file. It is a
text-based, human-readable format.

Installation Instructions
=========================

This package is pure Python and has no dependencies outside of the standard
library. The easist way to install is using ``easy_install`` from the
setuptools_ package.  This usually goes something like this::

	$ easy_install oldowan.phylip

or on a unix-like system, assuming you are installing to the main Python
``site-packages`` directory as a non-privileged user, this::

	$ sudo easy_install oldowan.phylip

You may also use the standard python distutils setup method. Download the
current source archive from the file list towards the bottom of this page,
unarchive it, and install. On Mac OS X and many other unix-like systems, having
downloaded the archive and changed to the directory containing this archive in
your shell, this might go something like::

	$ tar xvzf oldowan.phylip*
	$ cd oldowan.phylip*
	$ python setup.py install

Quick Start
===========

oldowan.phylip has an interface based on the standard Python ``file``.  Import
oldowan.phylip::

  >>> from oldowan.phylip import phylip

Read a PHYLIP format file::

  >>> for entry in phylip('sequences.phylip', 'r'):
  ...     print entry['name'], len(entry['sequence'])

A more cumbersome, but equivalent way of doing the above::

  >>> phylip_file = phylip('sequences.phylip', 'r')
  >>> for entry in phylip_file:
  ...     print entry['name'], len(entry['sequence'])
  >>> phylip_file.close()

Even more cumbersome, and if the PHYLIP file is large, potentially
memory-draining version (the previous two methods only read one entry at a time
from the file, this reads the whole file into memory at once)::

  >>> phylip_file = phylip('sequence.phylip', 'r')
  >>> entries = phylip_file.readentries()
  >>> phylip_file.close()
  >>> for entry in entries:
  ...     print entry['name'], len(entry['sequence'])

Read a string of PHYLIP format sequences::

  >>> phylip_string = open('sequences.phylip', 'r').read()
  >>> for entry in phylip(phylip_string, 's'):
  ...     print entry['name'], len(entry['sequence'])

Read a file object::

  >>> phylip_file = open('sequences.phylip', 'r')
  >>> for entry in phylip(phylip_file, 'f'):
  ...     print entry['name'], len(entry['sequence'])

Write to a file::

  >>> phylip_file = open('sequences.phylip', 'w')
  >>> phylip_file.write({'name':'Sequence1', 'sequence':'AGCTAGCT'})
  >>> phylip_file.close()

Release History
===============

0.1.0 (April 8, 2011)
    initial release of module.

.. _PHYLIP: http://evolution.genetics.washington.edu/phylip/
.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
