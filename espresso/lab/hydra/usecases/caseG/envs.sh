#!/usr/bin/env bash

export CASSANDRA=/home/dexity/danse-workspace/AbInitio/espresso/lab/hydra/usecases/caseG
export CASSANDRA_PATH=$CASSANDRA/bin

# Update $PATH
export PATH=$CASSANDRA_PATH:$PATH

# Update PYTHONPATH
export PYTHONPATH=$CASSANDRA:$PYTHONPATH