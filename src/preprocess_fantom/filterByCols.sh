#!/bin/bash
set -e

# filters by column #

grep -v '^#' $1 | cut -f1-7,$2
