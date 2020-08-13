#!/bin/bash -l

#$ -P riseprac

#$ -pe omp 1

#$ -l h_rt=1:00:00

#$ -m ea

#$ -N sim

#$ -j y
#$ -o log_sim.qlog

echo "============================================"
echo "Start date : $(date)"
echo "Job name : $JOB_NAME"
echo "Job ID: $JOB_ID $SGE_TASK_ID"
echo "simname : $1"
echo "cao : $2"
echo "runtime : $4"
echo "============================================"

module purge
module load python3/3.6.5
module load openmpi
module load neuron/7.6.7

a="${1}"

mpirun -np 1 ./x86_64/special -mpi -c "${a}" -c "${2}" -c "${3}" -c "${4}" main.py


