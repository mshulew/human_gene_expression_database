#!/usr/bin/env python3
# coding: utf-8

"""
preprocess FANTOM data
"""
  
import sys
import xml.etree.ElementTree as ET
import pandas as pd

if __name__ == "__main__":

    xml_path = sys.argv[1]
    count_path = sys.argv[2]
    ncbi_path = sys.argv[3]
    output_path = sys.argv[4]
    tree = ET.parse(xml_path)
    root = tree.getroot()

# create dictionary of sample and cell line
    sample_cl = {}
    for analytics in root:
        for assaygroup in analytics:
            for assaygroups in assaygroup:
                for assay in assaygroups:
                    if assaygroups.get('label').split(';')[0] == 'Jurkat, Clone E6-1': # clean up Jurkat label
                        sample_cl.setdefault(assay.text,'Jurkat')
                    elif assaygroups.get('label').split(';')[0] == 'Hep G2': # clean up Hep G2 label
                        sample_cl.setdefault(assay.text,'HepG2')
                    else:  
                        sample_cl.setdefault(assay.text,assaygroups.get('label').split(';')[0])

# import raw counts matrix
    count_matrix = []
    with open(count_path, 'r') as count_file:
        for line in count_file:
            if list(sample_cl.keys())[0] in line:
                line = line.splitlines()[0].split('\t')
                count_matrix.append([sample_cl[x] if x in list(sample_cl.keys()) else x for x in line])
                cell_line_list = [sample_cl[x] if x in list(sample_cl.keys()) else x for x in line]
            else:
                count_matrix.append(line.splitlines()[0].split('\t'))

# convert count matrix to pandas dataframe
    count_matrix_df = pd.DataFrame(count_matrix[1:],columns=count_matrix[0])

# import GeneIDs, Gene Symbols and Ensembl GeneIDs from ncbi database
    geneids = []
    with open(ncbi_path, 'r') as ncbi_db:
        for line in ncbi_db:
            if line[0] != '#':
                geneids.append([line.split('\t')[0],line.split('\t')[1],line.split('\t')[3]])

# convert ncbi data to pandas dataframe
    gene_df = pd.DataFrame(geneids,columns=['GeneID','GeneSymbol','Gene'])

# merge dataframes
    merged_df = pd.merge(gene_df,count_matrix_df, on='Gene', how='outer')

# remove rows with NA in any column
    count_matrix_df = merged_df.dropna()

# import list of cell lines (hardwired but needs to be imported from a file)
    cell_lines = ['HeLa','RAMOS','Jurkat','MCF-7','HepG2','K-562','A549','A-431']

# filter dataframe
    filtered_df = count_matrix_df[['Gene','GeneID','GeneSymbol'] + cell_lines]

# convert to list
    filtered_df.to_csv(output_path, sep='\t', index=False)
