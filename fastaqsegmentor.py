#!/usr/bin/python2.7

import sys 
def batch_iterator(iterator, batch_size) :
    """Returns lists of length batch_size.
 
    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.
 
    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True #Make sure we loop once
    while entry :
        batch = []
        while len(batch) < batch_size :
            try :
                entry = iterator.next()
            except StopIteration :
                entry = None
            if entry is None :
                #End of file
                break
            batch.append(entry)
        if batch :
            yield batch
            
from Bio import SeqIO
record_iter = SeqIO.parse(open(sys.argv[1]),"fastq")
for i, batch in enumerate(batch_iterator(record_iter, 100000)) :
    filename = "group_%i.fastq" % (i+1)
    handle = open(filename, "w")
    count = SeqIO.write(batch, handle, "fastq")
    handle.close()
    print "Wrote %i records to %s" % (count, filename)