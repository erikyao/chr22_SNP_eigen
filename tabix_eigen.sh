#!/bin/bash

# number of chunks to split into
#   do not exceed 9 because my `split` command is set to use 1-digit suffix (with option `-a 1` on line 20)
#   plus my workstation has only 8 CPU-cores, so 7 is a reasonable choice
N_CHUNKS=7  
N_CHROM=22  # ID of the chromosome

F_EIGEN="Eigen_hg19_noncoding_annot_chr${N_CHROM}.tab.bgz"

F_BED_PREFIX="mart_export_hg19_chr${N_CHROM}_SNP"  # prefix of the input BED filename
F_BED_FORMAT="bed"                                 # file extension of the input BED

# Specify the Tabix output filenames
F_OUT_PREFIX=${F_BED_PREFIX}
F_OUT_FORMAT="out"  # file extension of the tabix output

# The tabix output contain 33 columns (without a header), but we only need two of them, `Eigen-raw` and `Eigen-PC-raw`
# We will use `cut` command to extract columns of interested, and save in the .score file
F_SCORE_PREFIX=${F_BED_PREFIX}
F_SCORE_FORMAT="score"

F_LOG="mylog.txt"

# split into ${N_CHUNKS} files, `${F_BED_PREFIX}_0` to `${F_BED_PREFIX}_{N_CHUNKS}`
split -n l/${N_CHUNKS} -a 1 -d ${F_BED_PREFIX}.${F_BED_FORMAT} ${F_BED_PREFIX}_

# add the `.bed` extension to the split files
for (( i = 0; i < ${N_CHUNKS}; i++ ))
do 
    mv ${F_BED_PREFIX}_${i} ${F_BED_PREFIX}_${i}.${F_BED_FORMAT}
done

# run tabix for each split file (in background)
for (( i = 0; i < ${N_CHUNKS}; i++ ))
do 
    echo $(date --rfc-3339=seconds) "now running tabix on ${F_BED_PREFIX}_${i}.${F_BED_FORMAT}" >> ${F_LOG}
    tabix ${F_EIGEN} -R ${F_BED_PREFIX}_${i}.${F_BED_FORMAT} > ${F_OUT_PREFIX}_${i}.${F_OUT_FORMAT} &
done

echo $(date --rfc-3339=seconds) "now waiting..." >> ${F_LOG}
wait

# combine the tabix output into one file
find ${F_OUT_PREFIX}_*.${F_OUT_FORMAT} | sort | xargs cat > ${F_OUT_PREFIX}.${F_OUT_FORMAT}

See http://erikyao.github.io/2018/01/23/check-the-header-of-columbia-eigen-tab-delimited-files
  `chr` is the 1st column (counting from 1)
  `position` is the 2nd column
  `Eigen-raw` is the 30th column 
  `Eigen-PC-raw` is the 32th column
awk is applied to remove duplicate rows
cut -f1,2,30,32 ${F_OUT_PREFIX}.${F_OUT_FORMAT} | awk '!seen[$0]++' > ${F_SCORE_PREFIX}.${F_SCORE_FORMAT}

echo $(date --rfc-3339=seconds) "finished." >> ${F_LOG}