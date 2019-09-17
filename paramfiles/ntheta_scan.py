import numpy as np
from scan_gs2 import ONE, TWO

name = []
val = []
namelist = []
scandim = []

name.append('ntheta')
val.append(np.array([16,24,32,48,64,96,128]))
namelist.append('theta_grid_parameters')
scandim.append(ONE)
