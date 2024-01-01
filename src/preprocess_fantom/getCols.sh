#!/bin/bash
set -e

# get column numbers for cell lines of interest

grep -E "Hela|HEK293|MCF7|HepG2|Jurkat|A431|A549|MDA-MB-453|PC-3|HT-1080" $1 | grep -v -E "EGF|HRG" | awk '{print $1}' | tr '\n' ',' | rev | cut -c2- | rev
