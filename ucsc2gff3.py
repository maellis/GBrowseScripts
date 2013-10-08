"""
ucsc2gff3 converter
Author: Miandra Ellis
Aug 1, 2013

call from terminal using: ucsc2gff3 input.txt > ideogram.gff
"""
#!\usr\bin\python2.7
import sys

#variables
input_file = open(sys.argv[1],'r')

source	= "UCSC"
seqtype	= "cytoband"	
score 	= "."
strand	= "."
phase	= "."
name    = "."

print '##gff-version 3'

for line in input_file:
    source  = "UCSC"
    seqtype = "cytoband"    
    score   = "."
    strand  = "."
    phase   = "."
    name    = "."
    #skip comment lines that start with the '#' character
    if line.startswith("#") == False and len(line) != 1:
        #split line into columns by tab and strip whitespace. Returns list of file columns.
        data = line.strip().split('\t')

        #get field data
        seqid	= data[0]
        start	= data[1]
        end 	= data[2]
        name	= data[3]
        stain	= data[4]

        #insert necessary gff3 fields into list
        data.insert(1, source)
        data.insert(2, seqtype)
        data.insert(5, score)
        data.insert(6, strand)
        data.insert(7, phase)


        #replace the last column with a GFF formatted attributes columns
        data[8] = "Name=" + name + ";Parent=" + seqid + ";Stain="+ stain
        del  data[-1]

        #print out this new GFF line with tab delimeters
        print '\t'.join(data)
