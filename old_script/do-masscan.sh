#!/bin/bash

# do-masscan.sh (use with masscan)
# https://github.com/robertdavidgraham/masscan
#
# Scan for port 80 and 443 (websites) with masscan from the cidr file to produce an ip address list
# You need masscan (https://github.com/robertdavidgraham/masscan)
#
# first argument is the port
# second argument is the input file
#
# Author      : Samiux (http://www.infosec-ninjas.com)
# Date        : MAR 5, 2015
# Usage       : ./do-masscan.sh 443 cidr-us.txt
#
# 1st arg     : port 443
# 2nd arg     : cidr file from ip2location website
# output file : scan-banner-443.txt
#

while read line
do
	command="masscan $line -p $1 --banners -oL dummy.txt --max-rate 1000000 --excludefile exclude.txt"
	eval $command
	cat dummy.txt >> scan-all.txt
done < $2

# get ip address from scan-all.txt
cat scan-all.txt | grep banner >> list.txt
cat list.txt | cut -d" " -f4 >> newlist.txt

# delete "#masscan" and "# end"
sed --in-place "/#masscan/d" newlist.txt
sed --in-place "/# end/d" newlist.txt

# delete blank lines
sed --in-place "/^\s*$/d" newlist.txt

# remove dulplicate lines
awk '!a[$0]++' newlist.txt >> scan.txt

# remove files
rm list.txt
rm dummy.txt
rm scan-all.txt
rm newlist.txt

# rename filename with port number
mv scan.txt scan-banner-$1.txt

