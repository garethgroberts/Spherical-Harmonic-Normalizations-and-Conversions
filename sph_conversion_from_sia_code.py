import matplotlib.pyplot as plt
import numpy as np
import math
import pyshtools as pysh
import pygmt
import sys
import subprocess as sb

# code to take spherical harmonic output from sia ghelichkhan's code, re-normalize it to 
# a normalization that pyshtools can work with and plot. 
# if you want to compare the statistics of the original xyz file provided by forte (e.g. dyn-surf-FR2021-L100.xyz)
# to the new one (./SPH_REF_dyntopography.xyz) run ./plot_histo.gmt

cmd = " awk '{if (NR>4) print $2, $3, $4, $5}' < SPH_REF_dyntopography > SPH_REF_dyntopography_cut "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

# do the re-normalization to convert from sia's formatting to 4pi normalization, using / np.sqrt(4*np.pi)
coeffs_global = pysh.SHCoeffs.from_file('SPH_REF_dyntopography_cut', normalization='4pi', csphase = 1, lmax=100, format='shtools')  / np.sqrt(4*np.pi) 
coeffs_global.info()
grid_global = coeffs_global.expand(grid='DH2')
sia = grid_global.to_xarray()
sia.to_netcdf(path="./sia.nc")
pygmt.grd2xyz(grid="./sia.nc", output_type='file', outfile='./SPH_REF_dyntopography.xyz')

new_coeffs_arr = pysh.SHCoeffs.to_array(coeffs_global) 
pysh.shio.shwrite(filename='sia_conversion.sph', coeffs=new_coeffs_arr, lmax=100)
cmd = " awk -F',' '{print $3, $4}' < sia_conversion.sph > sia_real_no_cs.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))


# plotting      
fig = pygmt.Figure()
region="g"
proj="N0/8i"
frame=True
pygmt.makecpt(cmap="polar", series=[-6000, 6000, 1000], continuous=True)
fig.basemap(region=region, projection=proj, frame=frame)
fig.grdimage(grid='./sia.nc',region=region,projection=proj,frame=frame)
fig.plot(data="pb2002_boundaries.gmt", region=region, projection=proj, frame=frame, pen="1p,darkgrey")
fig.coast(shorelines="1p,black",area_thresh="100000")
fig.colorbar(frame=["x+lAmplitude, m"])
fig.show()
