#!/usr/bin/env python3
# coding: utf-8

"""
create count matrix of E-MTAB-2706 data
"""
  
import sys  
import xml.etree.ElementTree as ET
import pandas as pd

if __name__ == "__main__":

    xml_path = sys.argv[1]
    count_path = sys.argv[2]
    output_path = sys.argv[3]
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

# convert to pandas dataframe
    count_matrix_df = pd.DataFrame(count_matrix[1:],columns=count_matrix[0])

# import list of cell lines (hardwired but needs to be imported from a file)
    cell_lines = ['HeLa','RAMOS','Jurkat','MCF-7','HepG2','K-562','A549','A-431']

# filter dataframe
    filtered_df = count_matrix_df[['Gene'] + cell_lines]

# convert to list
    filtered_df.to_csv(output_path, sep='\t', index=False)
