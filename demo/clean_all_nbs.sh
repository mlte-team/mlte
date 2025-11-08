#!/usr/bin/env bash

# NOTE: this requires jq to be installed in the system.

DEMOS=$@
for demo in ${DEMOS[@]}
do
  for notebook_file in ${demo}/*.ipynb
  do
    source jq_clean_nb.sh "$notebook_file"
  done
  # Iterate over any notebooks in subfolders of the demos
  for subfolder_notebook_file in ${demo}/*/*.ipynb
  do
    echo $subfolder_notebook_file
    if [ -f "$subfolder_notebook_file" ]; then
      source jq_clean_nb.sh "$subfolder_notebook_file"
    fi
  done
done
