#!/bin/bash -l

for ca in 2 1
do
	qsub run_on_scc.sh $1 $ca -1 $2
done
