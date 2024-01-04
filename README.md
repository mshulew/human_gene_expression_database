# Human Gene Expression Resource
This repository is a collection of software to build a database of human gene expression data, annotations and other useful information.
The goal of this repository is to have a complete solution for extracting information of the expression of any human gene. It is intended to be useful to researchers who 
need to understand basic properties of human proteins (expression, molecular weight, etc.).

## Repository contents

File                                 | Description                                                                                       
------------------------------------ | ------------------------------------------------------------------------------------------------
src/scrape_ncbi_gene.py              | Python script to scrape https://www.ncbi.nlm.nih.gov/gene/. See below for usage  
ref/ncbi_complete_human_database.tsv | Output from scrape_ncbi_gene.py made on 12/13/2023                                                         
ref/ncbi_dataset.tsv                 | GeneID input list for scrape.ncbi_gene.py on 12/13/2023  

## Installation

You need to have Python3 installed on your machine. This project uses pyproject.toml to manage dependencies. To install the dependencies use pip:

```bash
pip -m install .
```

## Script description and usage
- ### src/scrape_ncbi_gene.py
  Python script for scraping https://www.ncbi.nlm.nih.gov/gene/.  
   Input file: List of NCBI GeneIDs. Can have multiple columns as long as the NCBI GeneID is in column 1  
  Output file: tsv files containing:  
  
  Column | Description
  -------|--------------------
  1      | NCBI GeneID
  2      | Gene Symbol
  3      | Gene Name
  4      | Ensembl GeneID
  5      | Synonyms (if included in entry)
  6      | Summary
  7      | Expression (if included in entry)

  Usage
  ```bash
  python src/scrape_ncbi_gene.py --g [path to GeneID list] --o [output path]
  
  optional:
  --help help

  to generate partial list: cat [path to output directory]/tmp/*
  ```

  If scraping is interrupted you can resume where you left off. Just rerun and use the same output directory (do not delete the output directory or its contents).
  

- ### src/preprocess_fantom/preprocess_fantom.sh
  bash script that processes FANTOM data to import into pandas

Usage
```bash
bash src/preprocess_fantom/preprocess_fantom.sh [path to FANTOM data] > [output tsv file]
```
preprocess_fantom.sh executes the following command:
- getSampleListTPM.sh or getSampleListCounts.sh, depending on file type (TPM or RAW COUNTS)
- cols=$(bash getCols.sh [ouitput from previous step])
- bash filterByCols.sh [path to FANTOM data] $cols
- bash removeNA.sh [output from previous step]


  

  
  
  
