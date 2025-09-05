#!/bin/bash

# script to convert alessandro forte's sph grid, which have format: l, m, real, imag
# to format for shtools: l, m, cos_coeff, sine_coeff
#
# gareth roberts july 2025

forte=./From_AForte230725/4Gareth/dyn-surf-FR2021-L100.lm 

awk '{print NR, $0}' < $forte > temp
awk '{if ($3==0) print $0}' < temp > temp1
awk '{if ($3!=0) printf "%d %d %d %.14f %.14f\n ", $1, $2, $3, sqrt(2) * $4, sqrt(2) * -1 * $5}' < temp > temp2
#awk '{if ($3!=0) print $1, $2, $3, sqrt(2) * $4, sqrt(2) * -1 * $5}' < temp > temp2
cat temp1 temp2 | sort -n -k1,1 | awk '{print $2, $3, $4, $5}' > recast.sph

python sph_conversion_to_sia_code.py

# copy the resultant spherical harmonic coefficients to propmat and run propmat (best to run propmat locally):
# cp dyn-surf-FR2021-L100_real_ggr.lm  /Users/grobert3/Documents/GRIC/Papers/Geoid_2023/fr22_geoid_scores_LMAX100/INPUT/RefGeo
# ./Users/grobert3/Documents/GRIC/Papers/Geoid_2023/fr22_geoid_scores_LMAX100/ggr_run.sh

# copy output from propmat back to this directory:
# cp /Users/grobert3/Documents/GRIC/Papers/Geoid_2023/fr22_geoid_scores_LMAX100/output_test0_LMAX100_RHOW1.03E+03_MIND0/SPH_REF_dyntopography ./


# convert spherical harmonic coefficients from propmat for use in pyshtools

# python sph_conversion_from_sia_code.py
# 
# rm -f temp temp1 temp2 temp.sph recast.sph forte_conversion.sph
# 
# # plotting of comparions
# 
# ./compare_sph_coeffs.gmt
# ./plot_forte_rowley22_sph.gmt
