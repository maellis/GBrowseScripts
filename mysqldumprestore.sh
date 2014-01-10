#! /bin/bash
# Author: Miandra Ellis
# Script for processing folder of mysql .dump or .sql files into databases.

user=root
password=CH4GEN

#Fill in with the path to the directory where the .dump file are.
dumpDirectory=

files="$(ls "$dumpDirectory")"

for file in $files; do 
	if [ "${file: -4}" == "dump" ]; then
		#Insert actual server name in place of localhost.
		mysql -u$user -p$password -h localhost "${file%.*}" <"$file";
	fi
done