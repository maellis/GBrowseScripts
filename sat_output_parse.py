#!/usr/bin/python2.7
#Author: Miandra Ellis
#Parse DAMBE output text files and create tab delimited excel sheet

import os, re

path = os.getcwd()

#variables
blockfound = False
count = 0
entry = ""

#regex objects
header = re.compile("Part I.")
IssObj = re.compile("Iss    ")
IsscObj = re.compile("Iss.c  ")
psymObj = re.compile("Prob ")
pasymObj = re.compile("Prob ")
pinvObj = re.compile("Prop. ")

class obj:
	def __init__(self):
		self.organism = ""
		self.pinv = ""
		self.Iss = ""
		self.Issc = ""
		self.psym = ""
		self.pasym = ""

	def __str__(self):
		return self.organism+'\t'+self.pinv+'\t'+self.Iss+'\t'+self.Issc+'\t'+self.psym+'\t'+self.pasym

# main method
for (path,dirs, files) in os.walk(path):
	for filename in files:
		if "Mboo" in filename:
			file_path = path + "/" + filename
			txt_file = open(file_path) # open file

			o = obj()
			o.organism = filename.strip('.txt')

			matchFound = False

			for line in txt_file:
				match2 = re.search(IssObj, line)
				match3 = re.search(IsscObj, line)
				match4 = re.search(psymObj, line)
				match5 = re.search(pasymObj, line)
				match6 = re.search(pinvObj, line)

				if match2:
					line = line.strip("Iss").strip()
					o.Iss = line

				if match3 and matchFound == False:
					matchFound = True
					line = line.strip("Iss.c").strip()
					o.Issc = line

				if match4 and o.psym != "" and o.pasym == "":
					line = line.strip("Prob (Two-tailed)").strip()
					o.pasym = line	

				if match4 and o.psym == "":
					line = line.strip("Prob (Two-tailed)").strip()
					o.psym = line

				if match6:
					line = line.strip("Prop. of invar.sites").strip()
					o.pinv = line

			print o	
			txt_file.close()