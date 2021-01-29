## Step 1: Download SNP Information from Biomart

Download SNPs on chr22 from BioMart (GRCH37.p13)

- Output file: `mart_export.txt`

Example records:

| Variant name	| Chromosome/scaffold name | Chromosome/scaffold position start (bp) | Chromosome/scaffold position end (bp) |
|---------------|--------------------------|-----------------------------------------|---------------------------------------|
|rs1285450127	|22	|16050001	|16050001|
|rs1442173437	|22	|16050005	|16050005|
|rs1569341485	|22	|16050005	|16050008|

## Step 2: Preprocess

Use script `preprocess.py`.

- Input file: `mart_export.txt`
- Output files:
  - `mart_export_hg19_chr22_SNP.bed`
  - `mart_export_hg19_chr22_SNP.rsID`

What does the script do?

- Coordinate system shift: Biomart use 1-based, while BED format is 0-based. The script shifts the coordinate system from 1-based to 0-based. (we always use 0-based in CERENKOV.)
- Some SNPs are longer than 1bp. The script removes such long SNPs because some feature extraction procedure cannot handle them.
- Input file `mart_export.txt` comes with a header. The script removes the header when saving the output.

## Step 3: Extract Eigen Scores

Use script `tabix_eigen.sh`.

- Requirement: `sudo apt install tabix`
- Input files:
  - SNP BED => `mart_export_hg19_chr22_SNP.bed`
  - Eigen => `Eigen_hg19_noncoding_annot_chr22.tab.bgz` + `Eigen_hg19_noncoding_annot_chr22.tab.bgz.tbi`
    - Downloadable from [http://files.cgrb.oregonstate.edu/Ramsey_Lab/cerenkov/genomewide/](http://files.cgrb.oregonstate.edu/Ramsey_Lab/cerenkov/genomewide/)
- Temporary Output:
  - Files ending with `.out` suffix, including:
    - Splitted `.out` files like `Eigen_hg19_noncoding_annot_chr22_1.out`
    - A combined `Eigen_hg19_noncoding_annot_chr22.out`
  - Splitted `.bed` files like `Eigen_hg19_noncoding_annot_chr22_1.bed`
- True output file: `Eigen_hg19_noncoding_annot_chr22.score`

What does the script do?

- Splits the `mart_export_hg19_chr22_SNP.bed` into 7 chunks
- Concurrently runs `tabix` on each chunk with the eigen `.tab.bgz` files to get the eigen scores in raw format, and then saves in `.out` files
- Combines all `.out` files and extract columns of interest, and then saves in the `.score` file

## Notes

- There is a `extract_eigen_columns.py` which can extract columns of interest from a `.out` file to a `.tsv` file.
  - It's function is covered in `tabix_eigen.sh` already.
  - Just in case if you need a `.tsv` for the eigen score
- `tabix_eigen.sh` will keep its tracks to a log file `mylog.txt`. (It may take up to 6 hours to finish so a log might be useful) 