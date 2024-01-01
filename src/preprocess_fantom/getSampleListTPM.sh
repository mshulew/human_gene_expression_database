#!/bin/bash
set -e

# creates list of samples with corresponding column number from FANTOM source data

a=7
while read line; do
	if [[ $line == *"]=TPM"* ]]; then
		(( a+=1 ))
		echo $line | awk -F 'tpm.' '{print $2}' | awk -F ']=' -v var="$a" '{print var,"\t",$1}' | 
			sed "s/%2b/+/g" | sed "s/%2c/,/g" | sed "s/%2e/./g" | sed "s/%2f/_/g" |
		        sed "s/%3a/:/g" | sed "s/%5e/Z/g" |	
			sed "s/%20/ /g" | sed "s/%27/'/g" | sed "s/%28/(/g" | sed "s/%29/)/g"
	fi
done <$1
