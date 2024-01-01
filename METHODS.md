# Comparing FANTOM and Expression Atlas expression atlas for a subset of genes

## Downloading datasets

**FANTOM**
```bash
# TPM
wget http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_v2/extra/CAGE_peaks_expression/hg38.cage_peak_phase1and2combined_fair_tpm_ann_fix1.osc.txt.gz
gunzip hg38.cage_peak_phase1and2combined_fair_tpm_ann_fix1.osc.txt.gz

# Raw counts
wget http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_v2/extra/CAGE_peaks_expression/hg38.cage_peak_phase1and2combined_fair_counts_ann.osc.txt.gz
gunzip hg38.cage_peak_phase1and2combined_fair_counts_ann.osc.txt.gz
```

**Expression Atlas**
```bash
# TPM
wget https://www.ebi.ac.uk/gxa/experiments-content/E-MTAB-2706/resources/ExperimentDownloadSupplier.RnaSeqBaseline/tpms.tsv

# Raw counts
wget https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/experiments/E-MTAB-2706/E-MTAB-2706-raw-counts.tsv.undecorated
# XML file with cell line names for samples (raw counts has sample names, not cell lines, and needs to be converted)
wget https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/experiments/E-MTAB-2706/E-MTAB-2706-configuration.xml
```
