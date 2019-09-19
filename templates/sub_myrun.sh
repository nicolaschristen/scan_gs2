#!/bin/bash
#SBATCH -N1 -n48     				# N for nodes (48 CPUs), n for cores
#SBATCH --time=05:00:00
#SBATCH --job-name=sub_myrun
#SBATCH --error sub_myrun.job.err      	        # error file
#SBATCH --output sub_myrun.job.out                # output file
#SBATCH --account=MY_ACCOUNT                  # account number (check with saldo -b --skl)
#SBATCH --partition=skl_fua_prod                # queue: skl_fua_prod, skl_fua_dbg (max. 4 nodes/30 min), skl_fua_bprod

srun -n 48 /path/to/gs2 myrun.in > myrun.txt
