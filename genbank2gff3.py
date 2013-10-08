#!/usr/bin/python2.7
# Author: Miandra Ellis
# Jun 26 2013
# Parse info from genbank file and output .gff3

import sys, os, re

gene_list = []
entry = ''
counter = 0
block_found = False

locus_tag = re.compile("/locus_tag=")
start_seq_tag = re.compile("<?[\\d]+[..]{2}>?[\\d]+>?")
phase_tag = re.compile("/codon_start=")
scaffold_tag = re.compile("(  gene  ) | (  CDS  ) | (  misc_feature  ) | (  tRNA  )")
dbxref_tag = re.compile("(/db_xref=)")
product_tag = re.compile ("(/product=)")
locus_header = re.compile("LOCUS")

class gene:
	def __init__(self):
		self.seqid = "chr"
		self.source = "genbank"
		self.gb_type = "."
		self.seq_start = "."
		self.seq_end = "."
		self.score = "."
		self.strand = "+"
		self.phase = "0"
		self.gene_name = ""
		self.db_xref = []
		self.note = ""

	def __str__(self):
		line = self.seqid+"\t"+self.source+"\t"+self.gb_type+"\t"+self.seq_start \
		  +"\t"+self.seq_end+"\t"+self.score+"\t"+self.strand+"\t"+self.phase+"\t"

		line += "Name=" + self.gene_name + ";"
		line += "Dbxref=" + ",".join(self.db_xref).replace("\"", "") + ";"

		if self.note:
			line += "Note=" + self.note + ";"
		line += "\n"
		return line

def parser(entry):
	""" Parses all of entry and returns a gene object that represents it."""
	is_db_xref = False
	is_product = False

	g = gene()
	entry = entry.split('\n')
	for line in entry:
		match = re.search(scaffold_tag, line)
		match1 = re.search(start_seq_tag, line)
		match2 = re.search(locus_tag, line)
		match3 = re.search(phase_tag, line)
		match4 = re.search(dbxref_tag, line)
		match5 = re.search(product_tag, line)
		
		if match and match1:
			line = line.replace(" ", "")
			if line.find("gene") >= 0:
				g.gb_type = "gene"
			elif line.find("CDS") >=0:
				g.gb_type = "CDS"
			elif line.find("misc_feature") >=0:
				g.gb_type = "misc_feature"
			elif line.find("tRNA") >=0:
				g.gb_type = "tRNA"
			
			if line.find("complement") >=0:
				g.strand = "-"

			seq = str(match1.group(0))

			g.seq_start = seq.split("..")[0].replace("\D", "")
			g.seq_end = seq.split("..")[1].replace("\D", "")

		if match2:
			g.gene_name = line.strip().strip("/locus_tag=")[1:-1]
			
		if match3:
			g.phase = line.strip().strip("/codon_start=")		

		if line.find("/") >= 0:
			is_product = False

		if is_db_xref:
			g.db_xref.append(line.strip().strip("\""))

		if is_product:
			g.note += line.strip().strip("\"")

		if match4: 
			g.db_xref.append(line.strip().strip("/db_xref="))

		if match5:
			if line.find("/product=") >= 0:
				g.note = line.strip().strip("/product=")[1:-1]
				is_product = True			
	return g

""" Main Function """
path = os.getcwd()
genbank_filename = sys.argv[1]
parse_me = open(path + "/" + genbank_filename)

for line in parse_me:
	match_obj = re.search(scaffold_tag, line)
	match_obj1 = re.search(locus_header, line)

	if match_obj1:
		acc_num = line.split()[1] 
	elif line.find("  source  ") >= 0:
		line = line.strip("  source  ").strip(" ")
		seq_id_ss, seq_id_se = line.split("..")	
	#Create entry and parse once next entry found.	
	elif match_obj:
		block_found = True
		if counter > 0: 
			gene_list.append(parser(entry))
			entry = ''
		counter += 1
		entry += line
	#If Origin is found parse the last entry created
	elif line.find('ORIGIN') >= 0:
		gene_list.append(parser(entry))
		break
	#Doesn't record information before first genbank entry is found
	else:
		if block_found == True:
			entry +=line

output = open(acc_num +".gff3", "w")
first_line = "##gff-version 3"
second_line = "##sequence-region %s %s %s" %("chr", seq_id_ss, seq_id_se)
output.write(first_line + "\n" + second_line + "\n")

for obj in gene_list:	
	output.write(obj.__str__())
	
output.close()
parse_me.close()