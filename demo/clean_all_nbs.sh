#!/usr/bin/env bash

# NOTE: this requires jq to be installed in the system.

#for file in ./scenarios/*.ipynb
#do
#  source jq_clean_nb.sh "$file"
#done

for file in ./simple/*.ipynb
do
  source jq_clean_nb.sh "$file"
done
