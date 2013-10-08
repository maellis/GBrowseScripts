import sys
#!/usr/bin/python2.7
# Author: Miandra Ellis
# Jul 18, 2013

file_list = list(sys.argv[3:])

for item in file_list:
    input_file = open(item,'r')
    print "Processing " + item

    output_file = open(item[:-4]+".gff3", 'w')
    output_file.write('##gff-version 3 \n')
    for line in input_file:
      #skip comment lines that start with the '#' character
      if line[0] != '#':
        #split line into columns by tab
        data = line.strip().split('\t')
        if len(data)== 9:
            # data[1] = data[1].split('_')[-1]
            data[1] = data[1].strip(sys.argv[1]+"_")
            if data[1].beginswith('_'):
                data[1]=data[1].strip('_')

            transcriptID = data[-1].split('transcript_id')[-1].split(';')[0].strip()[1:-1]
            geneID = data[-1].split('gene_id')[-1].split(';')[0].strip()[1:-1]

            #replace the last column with a GFF formatted attributes columns
            #I added a GID attribute just to conserve all the GTF data
            data[-1] = "Name=" + transcriptID

            #print out this new GFF line
            output_file.write('\t'.join(data))
            output_file.write('\n')
        else:
            data.insert(0,"chr")
            data.insert(1,str(sys.argv[3])[:-4])
            data.insert(2,"exon")
            data.insert(7,".")
            data[-1] = "Name=" + data[-1]
            output_file.write('\t'.join(data))
            output_file.write('\n')
    output_file.close()