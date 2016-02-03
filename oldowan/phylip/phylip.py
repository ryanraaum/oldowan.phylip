import re
import StringIO


class phylip(object):
    """Create a phylip file object::

        f = phylip(filename_or_data,[ mode="r"])

    The API for the phylip file object closely follows the interface of the
    standard python file object.

    The mode can be one of:

    * 'r' - reading (default)
    * 's' - string data
    * 'f' - file object
    * 'a' - append
    * 'w' - write

    The file will be created if it doesn't exist for writing or appending; it
    will be truncated when opened for reading.

    For read mode, universal newline support is automatically invoked.

    Each PHYLIP entry is parsed into a dict with 'name' and 'sequence' values.
    """

    __mode = None

    def __get_mode(self):
        return self.__mode

    mode = property(fget=__get_mode,
                    doc="file mode ('r', 's', 'f', 'w', or 'a')")

    def __get_closed(self):
        return self.__fobj.closed

    closed = property(fget=__get_closed,
                      doc="True if the file is closed")

    __fobj = None
    __buff = None
    __entries = None
    __cursor = 0
    __wrap_at = 80
    __endline = '\n'

    __ntax = None

    def __get_ntax(self):
        return self.__ntax

    ntax = property(fget=__get_ntax,
                    doc="number of taxa (integer)")

    __nchar = None

    def __get_nchar(self):
        return self.__nchar

    nchar = property(fget=__get_nchar,
                    doc="number of characters (integer)")

    def __init__(self, filename_or_data, mode='r', parse=True):
        """x.__init__(...) initializes x

        see x.__class__.__doc__ for signature"""

        if mode[0] in ['r', 'a', 'w']:
            if mode == 'r':
                # force universal read mode
                mode = 'rU'
            self.__fobj = open(filename_or_data, mode)
        elif mode == 'f':
            self.__fobj = filename_or_data
        elif mode == 's':
            self.__fobj = StringIO.StringIO(filename_or_data)
        else:
            msg = "mode string must start with 'r', 'a', 'w', 'f' or 's', \
                    not '%s'" % mode[0]
            raise ValueError(msg)
        self.__mode = mode
        self.parse = parse

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return self

    def __enter__(self):
        """__enter__() -> self."""
        return self

    def __exit__(self, type, value, traceback):
        """__exit__(*excinfo) -> None.  Closes the file."""
        self.close()

    def close(self):
        """close() -> None or (perhaps) an integer.  Close the file."""
        if self.__mode == 'w':
            self.__fobj.write(self.__header())
            self.__write_all()
        return self.__fobj.close()

    def __header(self):
        return '%d %d\n' % (self.ntax, self.nchar)

    def flush(self):
        """flush() -> None.  Flush the internal I/O buffer."""
        return self.__fobj.flush()

    def next(self):
        """next() -> the next entry, or raise StopIteration"""
        nxt = self.readentry()
        if nxt is None:
            raise StopIteration
        return nxt

    def read(self):
        """read() -> list of dict entries, reads the remainder of the data.

        Equivalent to readentries()."""
        return self.readentries()

    def readentry(self):
        """readentry() -> next entry, as a dict.

        Return None at EOF."""
        # Easist to parse the whole file at once.
        # Files in the PHYLIP format usually aren't large enough for this to be
        # a problem.
        if self.__entries is None:
            self.__parse()
        if self.__cursor < self.ntax:
            current = self.__entries[self.__cursor]
            self.__cursor = self.__cursor + 1
            return current
        return None

    def readentries(self):
        """readentries() -> list of entries, each a dict.

        Call readentry() repeatedly and return a list of the entries read."""
        return list(x for x in self)

    def write(self, entry, wrap_at=80, endline='\n'):
        """write(entry) -> None. Write entry dict to file.

        argument dict 'entry' must have keys 'name' and 'sequence', both
        with string values."""
        self.__wrap_at = wrap_at
        self.__endline = endline

        if not ('name' in entry and 'sequence' in entry):
            raise ValueError('entry missing either name or sequence')
        if self.__entries is None:
            self.__entries = []
            self.__ntax = 0
            self.__nchar = len(entry['sequence'])
        if len(entry['sequence']) != self.nchar:
            raise ValueError("Sequence length does not match")
        self.__ntax += 1 
        self.__entries.append(entry)

    def write_entries(self, entries):
        """write_entries(entries) -> None. Write list of entries to file.

        The equivalent of calling write for each entry."""
        for entry in entries:
            self.write(entry)

    def __parse(self):  
        self.__entries = []
        header = self.__fobj.readline()
        header_entries = header.split()
        if len(header_entries) != 2:
            raise ValueError("File does not have required header")
        (self.__ntax, self.__nchar) = [int(x) for x in header_entries]
        curr_nchar = 0
        first = True
        while curr_nchar < self.nchar:
            curr_nchar = self.__read_block(self.ntax, curr_nchar, first)
            first = False

    def __read_block(self, ntax, curr_nchar, first):
        for i in range(ntax):
            line_len = 0
            while line_len == 0:
                line = self.__fobj.readline().strip()
                line_len = len(line)
            line_len = 0
            if first:
                entry = {'name'     : line[:10].strip(),
                         'sequence' : ''.join(line[10:].split()) }
                self.__entries.append(entry)
            else:
                self.__entries[i]['sequence'] = \
                        self.__entries[i]['sequence'] + ''.join(line.split())
        return len(self.__entries[0]['sequence'])

    def __write_all(self):
        combined = [e['name'][:10].ljust(10) + e['sequence'] \
                    for e in self.__entries]
        broken = [split_string(s, self.__wrap_at, self.__endline) for s in combined]
        blocks = zip(*broken)
        for block in blocks:
            for entry in block:
                self.__fobj.write(entry)
            self.__fobj.write(self.__endline)


def split_string(s, wrap_at=80, endline='\n'):
    """split_string(s[, wrap_at[, endline]]) -> a list. 

    Given a string, split it every 'wrap_at' characters and append the
    stated 'newline'."""
    # for the wrapping, DON'T use 'textwrap.wrap'. It is very slow because
    # it tries to be clever and find word breaks to wrap at.
    exploded_seq = list(s)
    wrap_points = range(0, len(exploded_seq), wrap_at)
    wrap_points.reverse()
    for i in wrap_points[:-1]:
        exploded_seq.insert(i, '\n\t')
    exploded_seq.append('\n')
    s = ''.join(exploded_seq)
    return s.split('\t')
