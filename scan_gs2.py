import sys
import os

# Add path to directory where scan-files are stored
taskdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'paramfiles')
sys.path.insert(0, taskdir)

import f90nml as fnml
import numpy as np
import copy as cp
import fileinput as fin
from shutil import copyfile
import subprocess
import run_parameters as runpar
import importlib
from cst import ONE, TWO, NDIM_MAX

# Dict that will contain every parameter to scan
scan = {ONE:[],TWO:[]}

# From command-line arguments, get info about this analysis run (filenames, tasks to complete ...)
run = runpar.runobj()

# Import all parameters from paramfiles/myfile.py
pf = __import__(run.paramfile)

def main():

    # If nonlinear, make sure the user is aware of computing cost.
    check_if_nl(run)

    # Add all parameters to the current scan
    nparams = len(pf.name)
    for iparam in range(nparams):
        add_param_to_scan(scan, pf.name[iparam], pf.dim[iparam], pf.namelist[iparam], pf.scandim[iparam], pf.func[iparam])

    # Array containing all values of parameters higher in the scan tree
    valtree = [0*i for i in range(nparams)]

    # Generate new input files
    modify_files(run.base_name, valtree, scandim=ONE, patchin={})

class gs2_param:
    def __init__(self, var='', dim=np.array([]), in_list='', func=None):
        self.name = var
        self.dim = dim
        self.namelist = in_list
        self.func = func

def add_param_to_scan(scan, name, dim, namelist, scandim, func):
    newparam = gs2_param(name, dim, namelist, func)
    if scandim == ONE:
        scan[ONE].append(newparam)
    elif scandim == TWO:
        scan[TWO].append(newparam)
    else:
        sys.exit('ERROR: this code only supports up to '+NDIM_MAX+' dimensions for a scan.')

def get_filenames(fname):
    infile = fname + '.in'
    if run.scheduler == 'slurm':
        schedfile = 'sub_' + fname + '.sh'
        ppfile = 'pp_' + fname + '.sh'
    else:
        schedfile = 'sub_' + fname + '.pbs'
        ppfile = 'pp_' + fname + '.pbs'
    return infile, schedfile, ppfile

def increment_dim(scandim):
    if scandim == ONE:
        scandim = TWO
    else:
        scandim = END
    return scandim

def check_if_nl(run):
    orig_in_fname, dummmy1, dummy2 = get_filenames(run.base_name)
    infile = fnml.read(orig_in_fname)
    if infile['nonlinear_terms_knobs']['nonlinear_mode'] == 'on' \
            and run.launch_sims == True:
        choice = ''
        mssg = ("\nWARNING:\n\n"
                "You are about to run a scan of NONLINEAR gyrokinetic simulations.\n"
                "Those can be extremely expensive. Do you still wish to proceed ?\n"
                "'y'=Yes, 'n'=No:  ")
        while not (choice in ['y','n']):
            choice = input(mssg)
        if choice == 'n':
            sys.exit('\nExiting.\n')

def modify_files(fname, valtree, scandim, patchin):

    # Iterate over every set of values taken by parameters in this dimension of the scan.
    for ival in range(scan[scandim][0].dim):
    
        # Name-base and patch to be modified for this ival.
        my_fname = fname
        my_patchin = cp.deepcopy(patchin)

        # For every parameter in this dimension of the scan, modify the files.
        for iparam in range(len(scan[scandim])):
            # Append parameter to namelist for in-file patching
            var = scan[scandim][iparam].name
            val = scan[scandim][iparam].func(ival,valtree)
            nml = scan[scandim][iparam].namelist
            if not nml in my_patchin:
                my_patchin[nml] = {}
            my_patchin[nml][var] = val
            # Append parameter to the filenames
            my_fname = my_fname + '_' + var + '_' + str(val)
            # Update history tree
            if scandim == ONE:
                iparam_all = iparam
            if scandim == TWO:
                iparam_all = len(scan[ONE]) + iparam
            valtree[iparam_all] = val
        
        # If we are at the last dimension of the scan, then patch, save the files, and clear history tree.
        if scandim == run.ndim:
            orig_in_fname, orig_sched_fname, orig_pp_fname = get_filenames(run.base_name)
            new_in_fname, new_sched_fname, new_pp_fname = get_filenames(my_fname)
            # First in-file
            if run.save_in:
                fnml.patch(orig_in_fname, my_patchin, new_in_fname)
            # Then scheduling file
            if run.save_sched:
                copyfile(orig_sched_fname, new_sched_fname)
                with fin.FileInput(new_sched_fname, inplace=True) as schedfile:
                    for line in schedfile:
                        print(line.replace(run.base_name, my_fname), end='')
            # Then postprocessing file
            if run.save_pp:
                copyfile(orig_pp_fname, new_pp_fname)
                with fin.FileInput(new_pp_fname, inplace=True) as ppfile:
                    for line in ppfile:
                        print(line.replace(run.base_name, my_fname), end='')
            # Launch GS2 simulation
            if run.launch_sims:
                if run.scheduler == 'slurm':
                    subprocess.run(['sbatch', new_sched_fname])
                elif run.scheduler == 'pbs':
                    subprocess.run(['qsub', new_sched_fname])
            # Launch postprocessing
            if run.launch_pp:
                if run.scheduler == 'slurm':
                    subprocess.run(['sbatch', new_pp_fname])
                elif run.scheduler == 'pbs':
                    subprocess.run(['qsub', new_pp_fname])
        # Or move on to the next dimension of the scan by calling function recursively
        else:
            next_scandim = increment_dim(scandim)
            modify_files(my_fname, valtree, next_scandim, my_patchin)

# Execute main
if __name__ == '__main__':
    main()
