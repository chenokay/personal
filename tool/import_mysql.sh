#!/bin/bash

while read line
do
	mysql -h 127.0.0.1 -P 3306 -uroot -pbin729830  -e "use business_sale; $line"
done < sqls


