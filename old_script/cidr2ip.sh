#!/bin/bash

# Author     : Samiux (http://infosec-ninjas.com)
# Date       : MAR 5, 2015
#
# Description: Extract IP address from cidr file (from ip2location website)
#
# dependency : prips (apt-get install prips)
# Usage      : ./cidr2ip.sh cidr.txt ip.txt

while read line
do
	command="prips $line >> $2"
	eval $command
done < $1
