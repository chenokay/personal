#!/bin/bash

cat $1 | python  import_to_mysql.py > sqls

while read line
do
	mysql -h 127.0.0.1 -P 3306 -uroot -pbin729830  -e "use personal_page; $line"
done < sqls


