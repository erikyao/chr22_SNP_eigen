"""
The tabix output contain 33 columns (without a header), but we only need two of them, `Eigen-raw` and `Eigen-PC-raw`

This script read the tabix output, assign column names, and extract columns of interest
"""

import pandas as pd

INPUT_FN = "mart_export_hg19_chr22_SNP.out"
OUTPUT_FN = "mart_export_hg19_chr22_SNP_eigen_scores.tsv"

# The original Eigen column names
#   See http://erikyao.github.io/2018/01/23/check-the-header-of-columbia-eigen-tab-delimited-files
col_names = "chr position ref alt GERP_NR GERP_RS PhyloPri PhyloPla PhyloVer PhastPri " \
                "PhastPla PhastVer H3K4Me1 H3K4Me3 H3K27ac TFBS_max TFBS_sum TFBS_num OCPval " \
                "DnaseSig DnasePval FaireSig FairePval PolIISig PolIIPval ctcfSig ctcfPval " \
                "cmycSig cmycPval Eigen-raw Eigen-phred Eigen-PC-raw Eigen-PC-phred".split(" ")

eigen_dfm = pd.read_csv(INPUT_FN, sep="\t", header=None, names=col_names, dtype=str)
eigen_dfm.sort_values(by=["chr", "position"], inplace=True)

# Extract the two score columns, plus `chr`, `position` columns for joining with our feature matrix
eigen_dfm = eigen_dfm.loc[:, ["chr", "position", "Eigen-raw", "Eigen-PC-raw"]]
# Rename columns in consistency with our feature matrix 
eigen_dfm.rename(columns={"chr": "chrom", 
                          "Eigen-raw": "eigen_raw", 
                          "Eigen-PC-raw": "eigen_pc_raw"}, inplace=True)

eigen_dfm.drop_duplicates(inplace=True)

# The `chrom` columns in Eigen and Tabix output are without the "chr" prefix
#   however in our feature matrix, we do have this prefix
eigen_dfm.loc[:, 'chrom'] = eigen_dfm.loc[:, 'chrom'].apply(lambda x: "chr{}".format(x))

eigen_dfm.to_csv(OUTPUT_FN, sep="\t", header=True, index=False)