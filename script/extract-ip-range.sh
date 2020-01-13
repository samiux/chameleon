#!/bin/bash
# ./extract-ip-range.sh ocean-digital-sg.txt > in.txt

# IP range list option
while read -r line
do
	nmap -sL -n $line | grep 'Nmap scan report for' | cut -f 5 -d ' '
done < "$1"

# Single IP range option
#nmap -sL -n $1 | grep 'Nmap scan report for' | cut -f 5 -d ' '
