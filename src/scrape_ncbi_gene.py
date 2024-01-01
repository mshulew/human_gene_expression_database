#!/usr/bin/env python3
# coding: utf-8

"""
Builds local spreadsheet for all ncbi genes from a list of GeneIDs
Scrapes https://www.ncbi.nlm.nih.gov/gene
"""

import os
import sys
import shutil
from bs4 import BeautifulSoup
from urllib import request
import multiprocessing
import subprocess
import time

start_time = time.time()

def scrape(geneList,temp_path,output_path,total_entries,entries_to_process,entries_processed_at_start):
# function fed to multiprocessor - scrapes NCBI Gene
    
# get number of GeneIDs processed from files written to temporary path
    result = subprocess.run(['ls',temp_path], stdout=subprocess.PIPE)
    entries_processed = len(str(result.stdout).split()[0].split('\\n'))

# display progress after every 10 GeneIDs are processed
    if entries_processed/total_entries > 0.9:
        elapsed_time = time.time() - start_time
        estimated_time = ((entries_to_process/(entries_processed-entries_processed_at_start))*elapsed_time - elapsed_time)/60
        sys.stdout.flush()
        sys.stdout.write('\r{:,} entries processed out of {:,} | elapsed time: {} min | time remaining: {} min  '.format(entries_processed,total_entries,round(elapsed_time/60,0),round(estimated_time,0)))
        
    else:
        if entries_processed % 100 == 0:

            elapsed_time = time.time() - start_time
            estimated_time = ((entries_to_process/(entries_processed-entries_processed_at_start))*elapsed_time - elapsed_time)/60
            sys.stdout.flush()
            sys.stdout.write('\r{:,} entries processed out of {:,} | elapsed time: {} min | time remaining: {} min  '.format(entries_processed,total_entries,round(elapsed_time/60,0),round(estimated_time,0)))

# open website and get source
    geneID = geneList[0]
    page_to_scrape = 'https://www.ncbi.nlm.nih.gov/gene/{}'.format(geneID)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = request.Request(page_to_scrape, headers=hdr)

    
    try:
        page = request.urlopen(req, timeout=30)

# parse source
        mainpage = BeautifulSoup(page, 'html.parser')
        report_header = mainpage.find('div',class_="rprt-header")
        report_section = mainpage.find('div',class_="rprt-section-body")

        try:
            geneid = report_header.find('span',class_="geneid").get_text().split()[2].split(',')[0]
        except:
            geneid = 'Not Found'
        try:
            gene_name = report_section.get_text().split('Symbol\n')[1].split('provided')[0]
        except:
            gene_name = 'Not found'
        try:
            full_name = report_section.get_text().split('Full Name\n')[1].split('provided')[0]
        except:
            full_name = 'Not found'
        try:
            ensembl = report_section.get_text().split('Ensembl:')[1].split('\n')[0]
        except:
            ensembl = 'Not Found'
        try:
            synonyms = report_section.get_text().split('Also known as\n')[1].split('\n')[0]
        except:
            synonyms = 'None'
        try:
            summary = report_section.get_text().split('Summary\n')[1].split('\n')[0]
        except:
            summary = 'Not found'
        try:
            expression = report_section.get_text().split('Expression\n')[1].split('\n')[0]
        except:
            expression = 'Not found'

# write to file
        with open(temp_path + '/' + geneID + '.tsv', 'w')as output_file:
            output_file.write('{}\n'.format('\t'.join([geneid,gene_name,full_name,ensembl,synonyms,summary,expression])))

# return scraped data
        return [geneid,gene_name,full_name,ensembl,synonyms,summary,expression]

    except:
# if can not open connection, will return skipped GeneID
        with open(output_path + '/log', 'a') as log_file:
            log_file.write('page request failed {}\n'.format(page_to_scrape))
        return geneList
        pass
    
def main():

    print('*'*20)
    print('Build gene database')
    print('Mark Shulewitz 2023')
    print('*'*20)

    genelist_path = "NONE"
    output_path = 'NONE'
    helpMe = False

# get options
    if len(sys.argv) > 1:
        for a in range(len(sys.argv)):
            if sys.argv[a].lower() == '--g':
                genelist_path = sys.argv[a+1]
            elif sys.argv[a].lower() == '--o':
                output_path = sys.argv[a+1]
            elif sys.argv[a].lower() == '--h':
                helpMe = True
    else:
        print('Error 1: Missing arguments')
        exit()
        
    if helpMe:
        print('usage: python3.11 ncbi_gene_db --g [path to list of genes] --o [path to output directory]')
        exit()

    if genelist_path == 'NONE':
        print('Error 2: No list of genes provided')
        exit()

    if output_path == 'NONE':
        print('Error 2: No list of genes provided')
        exit()

# make output directory if it doesn't exist
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

# make temp directory
    temp_path = output_path + '/tmp'
    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)
                
# import gene list
    
    genelist = []  
    with open(genelist_path, 'r') as genes:
        for line in genes:
            if 'NCBI GeneID' not in line:
                genelist.append(line.splitlines()[0].split('\t'))
    total_geneids = len(genelist)
    print('total GeneIDs in list provided: {:,}'.format(total_geneids))

# check if temp files exist
    processed_geneids = []
    processed_output = []
    print('counting processed GeneIDs...')
    sys.stdout.write('\rGeneIDs processed: {:,}  '.format(0))
    files_counted = 0
    for filename in os.listdir(temp_path):
        if filename[-4:] == '.tsv':
            with open(temp_path + '/' + filename, 'r') as temp_file:
                files_counted += 1
                if files_counted%100 == 0:
                    sys.stdout.flush()
                    sys.stdout.write('\rGeneIDs processed: {:,}  '.format(files_counted))
                for line in temp_file:
                    processed_geneids.append(line.split('\t')[0])
                    processed_output.append(line.splitlines()[0].split('\t'))
    print('\nprocessed GeneIDs counted')
                    
    if len(processed_geneids) > 0:
        genelist = [e for e in genelist if e[0] not in processed_geneids]

        print('already processed GeneIDs: {:,}'.format(len(processed_geneids)))
        print('{:,} remaining GeneIDs to process'.format(len(genelist)))

# count number of GeneIDs to process and GeneIDs already processed
    geneids_to_process = len(genelist)
    geneids_processed = len(processed_geneids)

# create log file
    if 'log' in os.listdir(output_path):
        with open(output_path + '/log', 'a') as log_file:
            log_file.write('{}\n'.format('NCBI gene scrape continued ...'))
            log_file.write('Number of GeneIDs to process: {:,}\n'.format(total_geneids))
            log_file.write('Number of GeneIDs processed: {:,}\n'.format(geneids_processed))
    else:
        with open(output_path + '/log', 'w') as log_file:
            log_file.write('{}\n'.format('NCBI gene scrape log'))
            log_file.write('Number of GeneIDs to process: {:,}\n'.format(total_geneids))
            log_file.write('Number of GeneIDs processed: {:,}\n'.format(geneids_processed))
    
# scrape ncbi data using multiprocessing
    print('scraping gene data from ncbi (multiprocessing)...')

    pool_size =int(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(processes=pool_size)
    pool_outputs = pool.starmap(scrape,[(a,temp_path,output_path,total_geneids,geneids_to_process,geneids_processed) for a in genelist])

# combine fully processed GeneIDs and create new genelist of skipped GeneIDs
    genelist = []
    for pool_output in pool_outputs:
        if len(pool_output) > 3:
            processed_output.append(pool_output)
        else:
            genelist.append(pool_output)
    geneids_to_process = len(genelist)
    
# loop to process any skipped GeneIDs
    while geneids_to_process > 0:
        print('\nProcessing skipped GeneIDs...')
        single_outputs = []
        for a in genelist:
            single_outputs.append(scrape(a,temp_path,output_path,total_geneids,geneids_to_process,geneids_processed))

        genelist = []
        for single_output in single_outputs:
            if len(single_output) > 3:
                processed_output.append(single_output)
            else:
                genelist.append(single_output)
        geneids_to_process = len(genelist)

# create output file
    output_file_path = output_path + '/ncbi_db.tsv'
    with open(output_file_path,'w') as output_file:
        output_file.write('# ncbi human gene database\n')

# write to file
    with open(output_file_path, 'a') as output_file:
        for output in processed_output:
            output_file.write('{}\n'.format('\t'.join(output)))

# delete temp directory
    shutil.rmtree(temp_path)

    print('\n')


if __name__ == "__main__":

    main()

