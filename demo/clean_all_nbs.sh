#!/usr/bin/env bash

# NOTE: this requires jq to be installed in the system.

DEMOS=$@
for demo in ${DEMOS[@]}
do
  for notebook_file in ${demo}/*.ipynb
  do
    source jq_clean_nb.sh "$notebook_file"
  done
done
