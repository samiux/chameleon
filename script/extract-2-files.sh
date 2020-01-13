#!/bin/bash

# To split the large file to 200 thousands lines per file
# Usage : ./extract-2-files.sh in-sg-all.txt in-sg-
# will create in-sg-01 ....

split -l 200000 -d $1 $2

