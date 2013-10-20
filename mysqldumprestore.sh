#! /bin/bash
# Author: Miandra Ellis
# Script for processing folder of mysql .dump or .sql files into databases.

# echo "Enter mysql database user name followed by [ENTER]:"
# # read -s user 

# echo "Enter mysql password followed by [ENTER]"
# # read -s password
user=root
password=bunny

dumpDirectory=/home/miandra/Dropbox/GBrowse/UneditedUCSCFiles

files="$(ls "$dumpDirectory")"

for file in $files; do 
	if [ "${file: -4}" == "dump" ]; then
		# mysql -u$user -p$password -e "Create database ${file%.*};"
		mysql -u$user -p$password -h localhost "${file%.*}" <"$file";
	fi
done