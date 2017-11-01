#!/bin/bash
# Job name:
#SBATCH --job-name=to_memfix
#
# Partition:
#SBATCH --partition=savio
# 
# QoS (put into debug mode:
#SBATCH --qos=savio_normal
#
# Processors:
# Based off of here: https://www.rosettacommons.org/node/3597
#SBATCH --ntasks=480
#
# Mail user:
#SBATCH --mail-type=all
#SBATCH --mail-user=csumnicht@berkeley.edu
#
# Requeue:
#SBATCH --requeue

## Command(s) to run:
module load openmpi
module load python/3.2.3
module load mpi4py
module load pip
module load virtualenv/1.7.2

#Start virtual env
virtualenv venv
source venv/bin/activate

ICC=/global/software/sl-6.x86_64/modules/langs/intel/2013_sp1.4.211/bin/intel64/icc
STATS_DIR=/global/scratch/kzentner/to_memfix
GAME=test_games/toot_and_otto_bitstring.py

# env CC=$ICC pip-3.2 install bitarray
pip-3.2 install bitstring
pip-3.2 install cachetools

mpiexec python3 -OO -B solver_launcher.py -sd $STATS_DIR $GAME
