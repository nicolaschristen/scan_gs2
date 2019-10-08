import numpy as np
from math import pi
#from scan_gs2 import ONE, TWO

ONE='one'
TWO='two'

name = []
dim = []
namelist = []
scandim = []
func = []

shat = 1.7202
nlink = 5
dkx = 1.0
ky = np.array([0.2,0.5,0.8,1.0,1.5,2.0,2.5,3.0])
Nky = ky.size
y0 = 1/ky
y0 = np.around(y0,3)
jtwist = np.around(2*pi*shat/(dkx*y0))
jtwist = jtwist.astype(int)
Njtwist = jtwist.size
nx = np.around(jtwist*(nlink-1)*3/2 + 1)
nx = nx.astype(int)
Nnx = nx.size

name.append('y0')
dim.append(Nky)
namelist.append('kt_grids_box_parameters')
scandim.append(ONE)
def get_y0(ival,valtree):
    return y0[ival]
func.append(get_y0)

name.append('jtwist')
dim.append(Njtwist)
namelist.append('kt_grids_box_parameters')
scandim.append(ONE)
def get_jtwist(ival,valtree):
    return jtwist[ival]
func.append(get_jtwist)

name.append('nx')
dim.append(nx)
namelist.append('kt_grids_box_parameters')
scandim.append(ONE)
def get_nx(ival,valtree):
    return nx[ival]
func.append(get_nx)

