#!/bin/bash
set -e

# remove entries with NA for GeneID and UniProtID

awk '$5 != "NA"' $1 | awk '$7!="NA"' | cut -f5,7,8-
