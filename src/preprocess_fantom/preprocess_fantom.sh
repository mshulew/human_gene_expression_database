#!/bin/bash
set -e

# preprocess FANTOM data to import into pandas
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# make list of samples and corresponding column number
if [[ $1 == *"tpm"* ]]; then
	bash ${SCRIPT_DIR}/getSampleListTPM.sh $1 > sampleList0001

elif [[ $1 == *"counts"* ]]; then
	bash ${SCRIPT_DIR}/getSampleListCounts.sh $1 > sampleList0001
	
else
	echo "check input file"
fi

# create string of column numbers to filter
columnsToFilter=$(bash ${SCRIPT_DIR}/getCols.sh sampleList0001)
rm sampleList0001

# filter columns by number
bash ${SCRIPT_DIR}/filterByCols.sh $1 ${columnsToFilter} > filteredDataSet0002

# remove rows with no GeneID
bash ${SCRIPT_DIR}/removeNA.sh filteredDataSet0002
rm filteredDataSet0002

