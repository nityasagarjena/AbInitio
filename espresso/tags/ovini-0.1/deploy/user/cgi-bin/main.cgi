#!/usr/bin/env bash
EXPORT_ROOT=/home/user/exports/ovini
source $EXPORT_ROOT/config/envs.sh
cd $EXPORT_ROOT/cgi-bin && python main.py $@