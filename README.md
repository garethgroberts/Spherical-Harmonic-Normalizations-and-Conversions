# Spherical-Harmonic-Normalizations-and-Conversions
Convert spherical harmonic coefficients to other normalization conventions.

The files in this directory convert the spherical harmonic coefficients
from Forte & Rowley (2022), provided by A. Forte, from their complex 
form with the Condon-Shortley phase, to real form without the Condon-Shortley 
phase. The resultant coefficients can then be inserted into S. Ghelichkhan's 
propmat code (with an additional multiplicative sqrt(4pi) term), and
used in pyshtools. 

propmat = https://doi.org/10.5281/zenodo.12696774 (Ghelichkhan et al., 2024).
pyshtools = https://shtools.github.io/SHTOOLS/index.html (Wieczorek & Meschede, 2018). 

To run the code first look at: 

./recast_forte_coeffs_to_shtool_coeffs.sh
