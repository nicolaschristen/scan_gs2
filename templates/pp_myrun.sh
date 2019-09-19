#!/bin/bash
#SBATCH --nodes=1 --ntasks-per-node=1 --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --job-name=pp_myrun
#SBATCH --error pp_myrun.job.err      	        # error file
#SBATCH --output pp_myrun.job.out                # output file
#SBATCH --account=MY_ACCOUNT                  # account number (check with saldo -b --skl)
#SBATCH --partition=bdw_all_serial

source /path/to/venv/bin/activate
python my_postprocessing.py
