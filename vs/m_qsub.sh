#!/bin/bash -l

for ca in 2.0 1.9 1.8 1.7 1.6 1.5 1.4 1.3 1.2 1.1 1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1
do
	qsub run_on_scc.sh $1 $ca -1 $2
done
