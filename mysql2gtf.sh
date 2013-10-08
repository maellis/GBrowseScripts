#! /bin/bash
# Author: Miandra Ellis
# Script for getting information from UCSC tables to populate gtf files.

echo "Enter mysql database user name followed by [ENTER]:"
read -s user 

echo "Enter mysql password followed by [ENTER]"
read -s password

DBS="$(mysql -u$user -p$password -e "show databases;"| tr -d "|" | grep -v Database)"
echo "Databases are: "$DBS

for db in $DBS; do
	if [ "$db" != "information_schema" ] && [ "$db" != "mysql" ] && [ "$db" != "performance_schema" ]; then
		myresult="$(mysql -u$user -p$password -e "show tables from $db;"  |tr -d "|" | grep -v Tables_in_$db)"
		for table in $myresult; do
			if [ "${table: -5}" != "pwMaf" ]&&[ "$table" != "extFile" ]\
			&&[ "${table:0:4}" != "blas" ]&&[ "${table:0:4}" != "mult" ]&&[ "${table: -5}" != "Score" ] ; then
				description="$(mysql -u$user -p$password -e \
				"select column_name from information_schema.columns where table_name='$table';" \
				| grep -v column_name | grep -v -x chrom \
				| grep -v bin | tr '\n' '\t')"
				if [[ "$description" == *score* ]]; then
					echo 1 Processing "$table"
					mysql -u$user -p$password -e "Use $db; Select chromStart,chromEnd,score,strand,name from $table into outfile '/tmp/$table.gtf'"
				else
					echo 2 Processing "$table"
					mysql -u$user -p$password -e "Use $db; Select chromStart,chromEnd,name from $table into outfile '/tmp/$table.gtf'"
				fi
			fi
			gtf2gff3 $table $table.gtf
		done
	fi

done

echo "Enter desired destination directory followed by [ENTER]"
read directory

sudo rm /tmp/*.gtf
sudo mv /tmp/*.gff3 "$directory" 
