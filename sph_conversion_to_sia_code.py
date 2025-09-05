import matplotlib.pyplot as plt
import numpy as np
import math
import pyshtools as pysh
import pygmt
import sys
import subprocess as sb

# code to convert spherical harmonics given in quantum format (i.e. l, m, Re, Im; from alessandro forte) to pyshtools 
# format, with 4-pi, ortho or schmidt normalizations, and thence into the normalization used by sia ghelickhan
# in his geodynamic-propmat-main code. 
#
# gareth roberts july 2025

# now use pyshtools to work with the spherical harmonic coefficients, we are assuming 4pi normalization and that the cordon-shortley phase format is used by forte
coeffs_global = pysh.SHCoeffs.from_file('recast.sph', normalization='4pi', csphase = -1, lmax=100, format='shtools')
coeffs_global.info()
grid_global = coeffs_global.expand(grid='DH2')
forte = grid_global.to_xarray()
forte.to_netcdf(path="./forte.nc")
pygmt.grd2xyz(grid="./forte.nc", output_type='file', outfile='./fortegrd_FR21.xyz')

# convert normalization for insertion into propmat (note: no condon-shortley phase and extra sqrt{4pi})
new_coeffs = coeffs_global.convert(csphase=1, lmax=100, normalization='4pi') * np.sqrt(4*np.pi) / 1e3
new_coeffs.info()
grid_new = new_coeffs.expand(grid='DH2')
new_coeffs_arr = pysh.SHCoeffs.to_array(new_coeffs) 
pysh.shio.shwrite(filename='temp.sph', coeffs=new_coeffs_arr, lmax=100)
cmd = " awk -F',' '{print $3, $4}' < temp.sph > dyn-surf-FR2021-L100_real_ggr.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

# restrict output to L = 50. 
pysh.shio.shwrite(filename='temp.sph', coeffs=new_coeffs_arr, lmax=50)
cmd = " awk -F',' '{print $3, $4}' < temp.sph > dyn-surf-FR2021-L100_real_ggr_l50.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

# forte coeffs converted into real 4pi-normalizations with no condon-shortley phase (for comparison with coefficients output from propmat)
new_coeffs_global = coeffs_global.convert(csphase=1, lmax=100, normalization='4pi') 
new_coeffs_arr = pysh.SHCoeffs.to_array(new_coeffs_global) 
pysh.shio.shwrite(filename='forte_conversion.sph', coeffs=new_coeffs_arr, lmax=100)
cmd = " awk -F',' '{print $3, $4}' < forte_conversion.sph > forte_real_no_cs.lm "
output = sb.check_output(cmd, stderr=sb.STDOUT, shell=True)
sys.stdout.write('{}'.format(output))

# plot alessandro forte's grid  
fig = pygmt.Figure()
region="g"
proj="N0/8i"
frame=True
pygmt.makecpt(cmap="polar", series=[-6000, 6000, 1000], continuous=True)
fig.basemap(region=region, projection=proj, frame=frame)
fig.grdimage(grid="./forte.nc",region=region,projection=proj,frame=frame)
fig.plot(data="pb2002_boundaries.gmt", region=region, projection=proj, frame=frame, pen="1p,darkgrey")
fig.coast(shorelines="1p,black",area_thresh="100000")
fig.colorbar(frame=["x+lAmplitude, m"])
fig.show()





