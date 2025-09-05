import matplotlib.pyplot as plt
import numpy as np
import math
import pyshtools as pysh
import pygmt
import sys
import subprocess as sb

cmd = " awk '{if (NR>4) print $2, $3, $4, $5}' < SPH_REF_dyntopography > SPH_REF_dyntopography_cut "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

# sia's coeffs to 4pi normalization, using / np.sqrt(4*np.pi)
coeffs_sia = pysh.SHCoeffs.from_file('SPH_REF_dyntopography_cut', normalization='4pi', csphase = 1, lmax=100, format='shtools')  / np.sqrt(4*np.pi)
new_coeffs_arr = pysh.SHCoeffs.to_array(coeffs_sia) 
pysh.shio.shwrite(filename='sia_conversion.sph', coeffs=new_coeffs_arr, lmax=100)
cmd = " awk -F',' '{print $3, $4}' < sia_conversion.sph > sia_real_no_cs.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

grid_sia = coeffs_sia.expand(grid='DH2')
sia = grid_sia.to_xarray()

# forte coeffs
coeffs_forte = pysh.SHCoeffs.from_file('recast.sph', normalization='4pi', csphase = -1, lmax=100, format='shtools')
new_coeffs_forte = coeffs_forte.convert(csphase=1, lmax=100, normalization='4pi') 

new_coeffs_arr = pysh.SHCoeffs.to_array(new_coeffs_forte) 
pysh.shio.shwrite(filename='forte_conversion.sph', coeffs=new_coeffs_arr, lmax=100)
cmd = " awk -F',' '{print $3, $4}' < forte_conversion.sph > forte_real_no_cs.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

grid_forte = new_coeffs_forte.expand(grid='DH2')
forte = grid_forte.to_xarray()


#write out sia and forte girds
sia.to_netcdf(path="./sia.nc")
forte.to_netcdf(path="./forte.nc")

