#!/bin/bash
# Job name:
#SBATCH --job-name=mttt_test
#
# Partition:
#SBATCH --partition=savio
# 
# QoS (put into debug mode:
#SBATCH --qos=savio_debug
#
# Processors:
#SBATCH --nodes=4
#
# Mail user:
#SBATCH --mail-user=csumnicht@berkeley.edu

## Command(s) to run:
module load openmpi
module load python/3.2.3
module load mpi4py

mpiexec python3 solver_launcher.py --debug test_games/mttt.py
