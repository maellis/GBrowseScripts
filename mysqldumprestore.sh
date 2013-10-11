#! /bin/bash
# Author: Miandra Ellis
# Script for processing folder of mysql .dump or .sql files into databases.

echo "Enter mysql database user name followed by [ENTER]:"
read -s user 

echo "Enter mysql password followed by [ENTER]"
read -s password

dumpDirectory="/home/miandra/Dropbox/GBrowse/UneditedUCSCFiles"

files="$(ls "$dumpDirectory")"

for file in $files; do 
	if [ "${file: -4}" == "dump" ]; then
		mysql -u$user -p$password "${file%.*} < $dumpDirectory/$file;"
	fi
done