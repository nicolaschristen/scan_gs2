import sys
import argparse
from cst import ONE, TWO

class runobj:

    def __init__(self):

        # Set defaults
        self.paramfile = 'myfile'
        self.base_name = 'myname'
        self.scheduler = 'slurm'
        self.ndim = ONE
        self.save_in = True
        self.save_sched = True
        self.save_pp = True
        self.launch_sims = False
        self.launch_pp = False

        # Modify attributes according to command-line arguments.
        self.set_parameters()


    def set_parameters(self):

        args = self.get_commandline()

        if args.paramfile:
            self.paramfile = args.paramfile
        else:
            sys.exit("Please provide the name of the file in the folder \'paramfiles\' \
                    from which to read  all scan parameters (as an example, see the file \'ntheta.py\').")
        if args.base_name:
            self.base_name = args.base_name
        else:
            sys.exit('Please provide a base string to use when creating files. Select option -h for help.')
        if args.scheduler: self.scheduler = args.scheduler
        if args.ndim==1:
            self.ndim = ONE
        elif args.ndim==2:
            self.ndim = TWO
        if args.skip_in: self.save_in = False
        if args.skip_sched: self.save_sched = False
        if args.skip_pp: self.save_pp = False
        if args.launch_sims: self.launch_sims = True
        if args.launch_pp: self.launch_pp = True


    def get_commandline(self):

        parser = argparse.ArgumentParser(description = 'Creating files and/or launching simulations \
                and/or post-processing for GS2 scans.')

        parser.add_argument('-f', '--paramfile', 
                help = "Name of the file (without .py extension) in the folder \'paramfiles\' \
                        from which to read  all scan parameters (as an example, see the file \'ntheta.py\').")

        parser.add_argument('-b', '--base_name', 
                help = 'Base string to use when creating files. If the base name is \'myrun\', \
                        then the input, scheduler and post-processing files should respectively be named \
                        \'myrun.in\', \'sub_myrun.sh\' and \'pp_myrun.sh\'.')

        parser.add_argument('-d', '--ndim', nargs = '?', choices=[1,2],
                help = 'Number of dimensions in the scan. Within one single dimension, multiple \
                        parameters can be varied simultaneously (e.g. delt and nstep).')

        parser.add_argument('-q', '--scheduler', nargs = '?', choices = ['pbs', 'slurm'],
                help = 'Number of dimensions in the scan. Within one single dimension, multiple \
                        parameters can be varied simultaneously (e.g. delt and nstep).')

        parser.add_argument('-i', '--skip_in', action = 'store_true', default = False,
                help = 'Do not save in-files.')

        parser.add_argument('-s', '--skip_sched', action = 'store_true', default = False,
                help = 'Do not save sched-files.')

        parser.add_argument('-p', '--skip_pp', action = 'store_true', default = False,
                help = 'Do not save pp-files.')

        parser.add_argument('-S', '--launch_sims', action = 'store_true', default = False,
                help = 'Submit sched-files to launch GS2 simulations.')

        parser.add_argument('-P', '--launch_pp', action = 'store_true', default = False,
                help = 'Submit pp-files to launch post-processing.')
        
        args = parser.parse_args()
        
        return args
