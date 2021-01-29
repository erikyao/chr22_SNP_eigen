import pandas as pd

INPUT_FN = "mart_export.txt"
OUTPUT_BED_FN = "mart_export_hg19_chr22_SNP.bed"
OUTPUT_RSID_FN = "mart_export_hg19_chr22_SNP.rsID"

# Received from Steven; SNPs on chr22 (BioMart GRCH37.p13)
#   This file has a header
df = pd.read_csv(INPUT_FN, header=0, sep="\t")

# rename the columns 
df.columns = ["name", "chrom", "chromStart", "chromEnd"]

# only keep 1-bp SNPs 
df = df.loc[df.chromStart == df.chromEnd]

# make the coordinate system 0-based (same with BED files)
df.loc[:, "chromStart"] = df.loc[:, "chromStart"] - 1

# save as a BED file (without header)
#   column order is adjusted to BED format
df.to_csv(OUTPUT_BED_FN, sep="\t", columns=["chrom", "chromStart", "chromEnd", "name"], header=False, index=False)

# save as a column of rsIDs (without header)
df.to_csv(OUTPUT_RSID_FN, sep="\t", columns=["name"], header=False, index=False)